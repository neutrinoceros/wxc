import builtins
import inspect
import sys
from collections import defaultdict
from functools import lru_cache
from importlib import import_module
from platform import python_version
from types import BuiltinFunctionType
from typing import Any

if sys.version_info < (3, 8):
    import importlib_metadata as md
else:
    import importlib.metadata as md

if sys.version_info < (3, 10):
    from stdlib_list import in_stdlib
else:

    def in_stdlib(package_name):
        return package_name in sys.stdlib_module_names


from wxc.levensthein import levenshtein_distance

# sorted by decreasing order of priority
# the 'version' attribute *may* in some cases (e.g., platform.py) be a function
VERSION_ATTR_LOOKUP_TABLE = frozenset(("__version__", "VERSION", "version"))


def is_builtin(name: str) -> bool:
    return hasattr(builtins, name)


def is_builtin_func(obj: Any) -> bool:
    if isinstance(obj, str):
        obj = get_obj(obj)
    return isinstance(obj, BuiltinFunctionType)


def get_builtin_obj(name: str):
    return getattr(builtins, name)


def get_suggestions(obj, attr):
    suggestions = []
    for a in dir(obj):
        if levenshtein_distance(attr, a, max_dist=2) <= 2:
            suggestions.append(a)
    return suggestions


@lru_cache(maxsize=128)
def get_obj(name: str):
    if is_builtin(name):
        return get_builtin_obj(name)

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

    for attr in reversed(attrs):
        try:
            obj = getattr(obj, attr)
            name += f".{attr}"
        except AttributeError as exc:
            msg = f"{name} has no member '{attr}'."
            suggestions = get_suggestions(obj, attr)
            if len(suggestions) > 1:
                repr_suggestions = ", ".join(f"'{s}'" for s in suggestions)
                msg += f" The following near matches were found: {repr_suggestions}"
            elif len(suggestions) == 1:
                msg += f" Did you mean '{suggestions[0]}' ?"
            raise AttributeError(msg) from exc

    return obj


def get_sourcefile(obj):
    try:
        file = inspect.getfile(obj)
    except OSError:
        file = obj.__file__
    except TypeError:
        # this happens for instance with `math.sqrt`
        # because inspect.getsourcefile doesn't work on compiled code
        # the second condition is met for os.fspath
        if inspect.ismodule(obj) or is_builtin_func(obj):
            raise
        return get_sourcefile(inspect.getmodule(obj))
    return file


def get_sourceline(obj):
    return inspect.getsourcelines(obj)[1]


def get_version(package_name: str) -> str:
    package = get_obj(package_name)
    for version_attr in VERSION_ATTR_LOOKUP_TABLE:
        if hasattr(package, version_attr):
            retv = getattr(package, version_attr)
            if not isinstance(retv, str):
                # this conditional guards against rare cases like the builtin
                # platform module, platform.version being a function
                continue
            return retv

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

    obj = get_obj(name)

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
