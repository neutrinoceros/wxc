import sys

if sys.version_info.minor >= 8:
    import importlib.metadata as md
else:
    import importlib_metadata as md

import inspect
from collections import defaultdict
from functools import reduce
from importlib import import_module
from platform import python_version

from stdlib_list import in_stdlib

VERSION_ATTR_LOOKUP_TABLE = frozenset(("__version__", "VERSION"))


def get_obj(name: str):
    name_in = name
    attrs = []
    while name:
        try:
            obj = import_module(name)
            break
        except ImportError:
            name, _, attr = name.rpartition(".")
            attrs.append(attr)
    if not name:
        raise ImportError(name_in)
    if attrs:
        obj = getattr(obj, attrs.pop())

    # will raise AttributeError in case of missing attr
    return reduce(getattr, [obj, *attrs])


def get_sourcefile(obj):
    try:
        file = inspect.getfile(obj)
    except OSError:
        file = obj.__file__
    except TypeError:
        # this happens for instance with `math.sqrt`
        # because inspect.getsourcefile doesn't work on compiled code
        if inspect.ismodule(obj):
            raise
        return get_sourcefile(inspect.getmodule(obj))
    return file


def get_sourceline(obj):
    return inspect.getsourcelines(obj)[1]


def get_version(package_name: str) -> str:
    package = get_obj(package_name)
    for version_attr in VERSION_ATTR_LOOKUP_TABLE:
        if hasattr(package, version_attr):
            return getattr(package, version_attr)

    try:
        return md.version(package_name)
    except md.PackageNotFoundError:
        pass

    if in_stdlib(package_name):
        return f"Python {python_version()}"

    raise LookupError(
        "Could not determine version metadata from '{package_name}'"
    )


def get_full_data(name: str) -> dict:
    data = defaultdict(str)
    package_name, _, _ = name.partition(".")

    try:
        obj = get_obj(name)
    except (ImportError, AttributeError):
        return data

    try:
        source = get_sourcefile(obj)
    except RecursionError:
        source = ""

    try:
        lineno = get_sourceline(obj)
        source += f":{lineno}" if lineno else ""
    except (OSError, TypeError):
        pass

    if source:
        data["source"] = source

    try:
        data["version"] = get_version(package_name)
    except LookupError:
        pass

    data["in_stdlib"] = in_stdlib(package_name)

    return data
