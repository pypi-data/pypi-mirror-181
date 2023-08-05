"""
saxonhe4py - a Saxon HE packaged for Python.
"""
from pathlib import Path

from saxonhe4py._version import __version__, __version_tuple__, version, version_tuple

_PACKAGE_DIRECTORY = Path(__file__).parent
try:
    SAXON_HE = _PACKAGE_DIRECTORY.parent / "saxon_he"
    SAXON_HE_JAR = next(SAXON_HE.glob("saxon-he-[0-9]*.[0-9]*.jar"))
except StopIteration:
    err_message = f"Could not find file with pattern saxon-he-[0-9]*.[0-9]*.jar in {str(SAXON_HE)}"
    raise ModuleNotFoundError(err_message)

__all__ = [
    "__version__",
    "__version_tuple__",
    "version",
    "version_tuple",
    "SAXON_HE_JAR",
]
