import itertools
from string import Formatter
from typing import Any, Mapping, Sequence

from lenient_string_formatter._missing import MISSING


class DisposableLenientFormatter(Formatter):
    """The actual implementation of the lenient formatter.

    Due to the stateful nature of this implementation (i.e. the auto-numbering is handled by an internal counter), this class should not be reused, and is therefore private and used only by the public LenientFormatter class.
    """

    def __init__(self) -> None:
        self.indexer = itertools.count()
        self.stale = False
        self.used_args: set[str | int] = set()

    def vformat(
        self, format_string: str, args: Sequence[Any], kwargs: Mapping[str, Any]
    ) -> str:
        assert not self.stale, f"{type(self).__name__} must not be reused"
        self.stale = True
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
            return MISSING

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
        if obj is MISSING:
            return self._restore_unmatched(field_name, conversion, spec), False
        obj = self.convert_field(obj, conversion)
        new_spec, known = self._vformat_lenient(spec, args, kwargs, depth - 1)
        if not known:
            return self._restore_unmatched(field_name, conversion, spec), False
        self.used_args.add(arg_used)
        return self.format_field(obj, new_spec), True

    def _restore_unmatched(self, field: str, conversion: str | None, spec: str) -> str:
        result = field
        if conversion:
            result += f"!{conversion}"
        if spec:
            result += f":{spec}"
        return f"{{{result}}}"
