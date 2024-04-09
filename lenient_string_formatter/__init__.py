"""
.. include:: ../README.md
"""

import importlib.metadata as metadata

__version__ = metadata.version(__package__ or __name__)

from .lenient_formatter import LenientFormatter

__all__ = ("LenientFormatter", "__version__")
