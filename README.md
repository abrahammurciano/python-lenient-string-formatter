# lenient-string-formatter

A lenient string formatter that leaves unmatched fields untouched in the output string instead of raising exceptions.

The following exceptions that are normally raised by the built-in string formatter are caught and handled as follows:

- KeyError and IndexError will not be raised if a field in the template is not matched by the arguments. Instead, the field will be left untouched in the output string.
- ValueError in case numbered and auto-numbered fields are mixed in the template (e.g. "{1} {}") will not be raised. Explicitly numbered fields will be matched according to their index (remaining untouched if the index is out of bounds), while auto-numbered fields will be matched according to their order in the arguments (again, remaining untouched if the index is out of bounds) independent of the explicit numbering.
- KeyError is not raised on unnumbered field with key/attribute access. (https://bugs.python.org/issue27307)

## Installation

You can install this package with pip.
```sh
$ pip install lenient-string-formatter
```

## Links

[![Documentation](https://img.shields.io/badge/Documentation-C61C3E?style=for-the-badge&logo=Read+the+Docs&logoColor=%23FFFFFF)](https://abrahammurciano.github.io/python-lenient-string-formatter)

[![Source Code - GitHub](https://img.shields.io/badge/Source_Code-GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=%23FFFFFF)](https://github.com/abrahammurciano/python-lenient-string-formatter.git)

[![PyPI - lenient-string-formatter](https://img.shields.io/badge/PyPI-lenient_string_formatter-006DAD?style=for-the-badge&logo=PyPI&logoColor=%23FFD242)](https://pypi.org/project/lenient-string-formatter/)

## Usage

This package provides a function called `lformat` that you can use to format strings in a lenient way. You can use it in the same way as you would use Python's built-in `str.format` method.

This package also provides the `LenientFormatter` class, a subclass of Python's built-in `string.Formatter`. It is used internally by the `lformat` function, but it can be used directly or subclassed if you need more control over the formatting process.

The examples below will use the `lformat` function. `LenientFormatter().format` can be used in the same way.

### Basic example

```python
from lenient_string_formatter import lformat

template = "{} {} {a} {b}"
formatted = lformat(template, 1, 2, a=3, b=4)
assert formatted == "1 2 3 4"
```

### Unmatched fields

Unmatched fields are left untouched instead of raising exceptions.

```python
template = "{} {} {a} {b}"
formatted = lformat(template, 1, a=3)
assert formatted == "1 {} 3 {b}"
```

### Mixing numbered and auto-numbered fields

Explicitly numbered fields are matched according to their index, while auto-numbered fields are matched according to their order in the arguments. They are matched independently of each other.

```python
template = "{1} {}"
formatted = lformat(template, 1, 2)
assert formatted == "2 1"
```

### Unnumbered field with key/attribute access

The built-in formatter raises a KeyError when an unnumbered field is used with key/attribute access. This is a bug in the built-in formatter (https://bugs.python.org/issue27307). This implementation doesn't have this bug.

```python
from types import SimpleNamespace

template = "{.attr} {[0]}"
formatted = lformat(template, SimpleNamespace(attr=1), [2])
assert formatted == "1 2"
```

### Format specifiers and conversion flags for unmatched fields

Unmatched fields are left untouched. This includes any format specifiers and conversion flags that are applied to the field. Furthermore, if the field is matched but the format specifier has a field which is unmatched, or vice versa, the field is still left untouched.

For example, below `{a:3}` and `{b!r}` have no matching values, and neither `c=3` nor `f=4` provide enough values to completely fill the fields `{c:{d}}` and `{e:{f}}`, so all fields are left untouched.

```python
template = "{a:3} {b!r} {c:{d}} {e:{f}}"
formatted = lformat(template, c=3, f=4)
assert formatted == template
```