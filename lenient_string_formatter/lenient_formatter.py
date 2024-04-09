from string import Formatter


class LenientFormatter(Formatter):
    """A lenient string formatter that leaves unmatched fields untouched in the output string instead of raising a KeyError."""
