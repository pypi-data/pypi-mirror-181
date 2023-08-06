"""Flywheel storage library."""
from importlib.metadata import version

from .errors import *
from .storage import Storage, get_storage

__version__ = version(__name__)

# pylint: disable=duplicate-code
__all__ = [
    "FileExists",
    "FileNotFound",
    "IsADirectory",
    "NotADirectory",
    "PermError",
    "Storage",
    "StorageError",
    "get_storage",
]
