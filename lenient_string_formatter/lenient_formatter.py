from __future__ import annotations

import itertools
from dataclasses import dataclass
from string import Formatter
from typing import Any, Mapping, Self, Sequence


class LenientFormatter(Formatter):
    """A lenient string formatter that leaves unmatched fields untouched in the output string instead of raising exceptions.

    The following exceptions that are normally raised by the built-in string formatter are caught and handled as follows:

    - KeyError and IndexError will not be raised if a field in the template is not matched by the arguments. Instead, the field will be left untouched in the output string.
    - ValueError in case numbered and auto-numbered fields are mixed in the template (e.g. "{1} {}") will not be raised. Explicitly numbered fields will be matched according to their index (remaining untouched if the index is out of bounds), while auto-numbered fields will be matched according to their order in the arguments (again, remaining untouched if the index is out of bounds) independent of the explicit numbering.
    - KeyError is not raised on unnumbered field with key/attribute access. (https://bugs.python.org/issue27307)
    """

    def vformat(
        self, format_string: str, args: Sequence[Any], kwargs: Mapping[str, Any]
    ) -> str:
        return _DisposableLenientFormatter().vformat(format_string, args, kwargs)


class _DisposableLenientFormatter(Formatter):
    """The actual implementation of the lenient formatter.

    Due to the stateful nature of this implementation (i.e. the auto-numbering is handled by an internal counter), this class should not be reused, and is therefore private and used only by the public LenientFormatter class.
    """

    def __init__(self) -> None:
        self.indexer = itertools.count()
        self._stale = False
        self.used_args = set()

    def vformat(
        self, format_string: str, args: Sequence[Any], kwargs: Mapping[str, Any]
    ) -> str:
        assert not self._stale, f"{type(self).__name__} must not be reused"
        self._stale = True
        result, _ = self._vformat_lenient(format_string, args, kwargs, 2)
        self.check_unused_args(self.used_args, args, kwargs)
        return result

    def get_value(
        self, key: str | int, args: Sequence[Any], kwargs: Mapping[str, Any]
    ) -> Any:
        try:
            return super().get_value(
                key if key != "" else next(self.indexer), args, kwargs
            )
        except (IndexError, KeyError):
            return _MISSING

    def _vformat_lenient(
        self,
        format_string: str,
        args: Sequence[Any],
        kwargs: Mapping[str, Any],
        depth: int,
    ) -> tuple[str, bool]:
        if depth < 0:
            raise ValueError("Max string recursion exceeded")
        result: list[tuple[str, bool]] = []
        for literal_text, field_name, spec, conversion in self.parse(format_string):
            result.append((literal_text, True))
            if field_name is None:
                continue
            assert spec is not None
            result.append(
                self._replace_field(field_name, conversion, spec, args, kwargs, depth)
            )
        return "".join(part for part, _ in result), all(known for _, known in result)

    def _replace_field(
        self,
        field_name: str,
        conversion: str | None,
        spec: str,
        args: Sequence[Any],
        kwargs: Mapping[str, Any],
        depth: int,
    ) -> tuple[str, bool]:
        obj, arg_used = self.get_field(field_name, args, kwargs)
        if obj is _MISSING:
            return str(_Unmatched(field_name, conversion, spec)), False
        obj = self.convert_field(obj, conversion)
        new_spec, known = self._vformat_lenient(spec, args, kwargs, depth - 1)
        if not known:
            return str(_Unmatched(field_name, conversion, spec)), False
        self.used_args.add(arg_used)
        return self.format_field(obj, new_spec), True


class _Missing:
    """Objects representing a field that could not be matched by the arguments and are to be left untouched."""

    def __getitem__(self, key: object) -> Self:
        return self

    def __getattr__(self, attr: str) -> Self:
        return self


_MISSING = _Missing()


@dataclass
class _Unmatched:
    name: str
    conversion: str | None
    spec: str

    def __str__(self) -> str:
        result = f"{self.name}"
        if self.conversion:
            result += f"!{self.conversion}"
        if self.spec:
            result += f":{self.spec}"
        return f"{{{result}}}"
