from __future__ import annotations

import builtins
import re
import sys
from collections import defaultdict
from functools import lru_cache
from types import BuiltinFunctionType

from wxc.levenshtein import levenshtein_distance

if False:
    # typecheck only
    from collections.abc import Iterable  # type: ignore [unreachable]
    from typing import Any, TypedDict

    class FullDataDict(TypedDict):
        source: str | None
        version: str
        in_stdlib: bool


# sorted by decreasing order of priority
VERSION_ATTR_LOOKUP_TABLE = ("__version__", "VERSION", "version")


def is_builtin(name: str) -> bool:
    return hasattr(builtins, name)


def is_builtin_func(obj: Any) -> bool:
    if isinstance(obj, str):
        obj = get_obj(obj)
    # this heuristic is equivalent to inspect.isbuiltin()
    # it should be noted that the type 'BuiltinFunctionType' isn't reserved
    # to the standard library, but is characteristic of functions that
    # are "written in C". See
    # https://docs.python.org/3/library/types.html?highlight=builtinfunctiontype#types.BuiltinMethodType
    return isinstance(obj, BuiltinFunctionType)


def get_builtin_obj(name: str):
    return getattr(builtins, name)


def get_suggestions(
    candidates: Iterable[str], target: str, *, max_dist: int = sys.maxsize
) -> list[str]:
    suggestions: dict[int, list[str]] = defaultdict(list)
    minimal_distance: int = max_dist
    for a in candidates:
        d: int = levenshtein_distance(target, a, max_dist=minimal_distance)
        if d <= minimal_distance:
            suggestions[d].append(a)
            minimal_distance = d
    return sorted(suggestions[minimal_distance])


@lru_cache(maxsize=128)
def get_objects(name: str) -> list:
    if is_builtin(name):
        return [get_builtin_obj(name)]

    from importlib import import_module

    name_in = name
    attrs = []
    objects = []
    while name:
        try:
            obj = import_module(name)
            break
        except ImportError:
            name, _, attr = name.rpartition(".")
            attrs.append(attr)
    if not name:
        raise ImportError(name_in)

    objects.append(obj)

    for attr in reversed(attrs):
        try:
            obj = getattr(obj, attr)
        except AttributeError as exc:
            msg = exc.args[0]
            # force the name to match the one specified by the user even
            # in cases where they are using an alias (for instance os.path is a alias for posixpath on UNIX)
            msg = re.sub(r"\'[^-\s]*\'", f"{name!r}", msg, count=1)
            suggestions = get_suggestions(dir(obj), attr)
            if len(suggestions) > 1:
                repr_suggestions = ", ".join(f"{s!r}" for s in suggestions)
                msg += f". Here are the closest matches: {repr_suggestions}"
            elif len(suggestions) == 1:
                msg += f". Did you mean {suggestions[0]!r} ?"
            raise AttributeError(msg) from exc
        else:
            name += f".{attr}"
            objects.append(obj)

    return objects


def get_obj(name: str):
    # for backwards compatibility
    return get_objects(name)[-1]


def get_sourcefile(obj):
    import inspect

    try:
        file = inspect.getfile(obj)
    except OSError:
        file = obj.__file__
    except TypeError:
        # this happens for instance with `math.sqrt`
        # because inspect.getfile doesn't work on compiled code
        # the second condition is met for os.fspath
        if (
            inspect.ismodule(obj)
            or is_builtin_func(obj)
            or inspect.getmodule(obj) is builtins
            or isinstance(obj, property)
        ):
            raise
        return get_sourcefile(inspect.getmodule(obj))
    return file


def get_sourceline(obj):
    import inspect

    return inspect.getsourcelines(obj)[1]


def get_version(
    package_name: str, *, _version_attr_lookup_table=VERSION_ATTR_LOOKUP_TABLE
) -> str:
    package = get_obj(package_name)
    for version_attr in _version_attr_lookup_table:
        if hasattr(package, version_attr):
            retv = getattr(package, version_attr)
            if not isinstance(retv, str):
                # this conditional guards against rare cases like the builtin
                # platform module, platform.version being a function
                continue
            return retv

    import importlib.metadata as md

    try:
        return str(md.version(package_name))
    except md.PackageNotFoundError:
        pass

    if package_name in sys.stdlib_module_names:
        from platform import python_version

        return f"Python {python_version()}"

    raise LookupError(f"Could not determine version metadata from {package_name!r}")


def get_full_data(name: str) -> FullDataDict:
    package_name, _, _ = name.partition(".")

    objects = get_objects(name)
    _d_source: str | None = None

    for obj in reversed(objects):
        try:
            source = get_sourcefile(obj)
        except RecursionError:
            pass
        except TypeError as exc:
            if "built-in module" in str(exc):
                # see https://github.com/neutrinoceros/wxc/issues/233
                _d_source = "built-in"
                break
            elif isinstance(obj, property):
                # as of Python 3.11, inspect.getfile doesn't have support for properties
                # but we're not making this a hard failure in case it is added in the future
                # and we fallback to finding out the sourcefile of the class itself
                continue
            else:
                raise
        else:
            try:
                lineno = get_sourceline(obj)
            except (OSError, TypeError):
                pass
            else:
                source += f":{lineno}" if lineno else ""
                break
            finally:
                _d_source = source

    try:
        _d_version = get_version(package_name)
    except LookupError:
        _d_version = "unknown"

    return {
        "source": _d_source,
        "version": _d_version,
        "in_stdlib": package_name in sys.stdlib_module_names,
    }
