from typing import Self


class _Missing:
    """Objects representing a field that could not be matched by the arguments and are to be left untouched."""

    def __getitem__(self, key: object) -> Self:
        return self

    def __getattr__(self, attr: str) -> Self:
        return self


MISSING = _Missing()
