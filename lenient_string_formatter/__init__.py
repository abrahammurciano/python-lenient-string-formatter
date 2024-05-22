"""
.. include:: ../README.md
"""

from string import Formatter
from typing import Any, Mapping, Sequence

from lenient_string_formatter._disposable_lenient_formatter import (
    DisposableLenientFormatter,
)


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
        return DisposableLenientFormatter().vformat(format_string, args, kwargs)


_formatter = LenientFormatter()


def lformat(format_string: str, *args: Any, **kwargs: Any) -> str:
    """Format a string with lenient formatting.

    This function is a convenience wrapper around the LenientFormatter class.

    Args:
        format_string: The format string to be formatted.
        *args: The positional arguments to be used for formatting.
        **kwargs: The keyword arguments to be used for formatting.
    """
    return _formatter.format(format_string, *args, **kwargs)


__all__ = ("LenientFormatter", "lformat")
