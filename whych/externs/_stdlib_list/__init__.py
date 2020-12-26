from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

# Import all the things that used to be in here for backwards-compatibility reasons
from .base import (
    get_canonical_version,
    in_stdlib,
    long_versions,
    short_versions,
    stdlib_list,
)
