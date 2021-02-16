import inspect
import os
import subprocess
import sysconfig
from datetime import datetime
from importlib import import_module
from itertools import accumulate
from pathlib import Path
from platform import python_version
from types import ModuleType
from typing import List, Optional, Union

from .externs._stdlib_list import in_stdlib


class Scope(dict):
    """
    A `Scope` is a Python code object that can be imported and/or called from an
    importable super-scope.
    Packages, modules, classes, functions and class methods qualify.
    """

    def __init__(self, n: Optional[Union[str, bytes]] = None):
        if n is not None:
            self.from_name(str(n))

    def from_name(self, scope_name: str):

        parts = scope_name.split(".")

        self["scope_name"] = scope_name
        self["package_name"] = parts[0]
        self["is_stdlib"] = in_stdlib(self["package_name"])

        idx = 0
        name_candidates = list(accumulate(parts, lambda x, y: ".".join([x, y])))
        for name in reversed(name_candidates):
            try:
                module = import_module(name)
                self["is_available"] = True
                break
            except ModuleNotFoundError:
                idx += 1
                continue
        else:
            self["is_available"] = False
            return

        self["module_name"] = module.__name__
        self["is_module"] = name == scope_name and inspect.ismodule(module)

        self._set_version(module)
        self["path"] = self.resolve_path(module)

        try:
            obj = import_module(parts[0])
            if len(parts) > 1:
                for part in parts[1:]:
                    obj = getattr(obj, part)

            self["line"] = inspect.getsourcelines(obj)[1]
        except (TypeError, OSError, AttributeError):
            pass

        ts = int(os.path.getmtime(self["path"]))
        self["last_updated"] = datetime.utcfromtimestamp(ts).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        try:
            os.chdir(Path(self["path"]).parent)
            process = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            hash = process.stdout.decode("utf-8")
            self["git_hash"] = hash.replace("\n", "")
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

    def _set_version(self, module):
        try:
            # this is standard in Python 3.8 and pip-installable otherwise
            import importlib.metadata as md
        except ImportError:
            md = None  # type: ignore
        ver = self._lookup(
            module,
            attrs=["__version__", "VERSION"],
            stdlib_default=f"python {python_version()}",
        )
        if ver is None and md is not None:
            try:
                ver = md.version(self["package_name"])
            except md.PackageNotFoundError:
                pass
        if ver:
            self["version"] = ver

    def resolve_path(self, module: ModuleType) -> Optional[str]:
        try:
            return inspect.getabsfile(self["module_name"])
        except TypeError:
            return self._lookup(
                module,
                attrs=["__file__", "__path__"],
                stdlib_default=sysconfig.get_paths()["stdlib"],
            )

    def _lookup(
        self, module: ModuleType, attrs: List[str], stdlib_default: str
    ) -> Optional[str]:

        for attr in attrs:
            try:
                ret = getattr(module, attr)
                if not isinstance(ret, str):
                    raise LookupError(
                        f"Unexpected return value ret={ret}, with type {type(ret)}"
                    )
                return ret
            except AttributeError:
                pass

        if self["is_stdlib"]:
            return stdlib_default

        return None

    def __str__(self):
        lines = [f"{attr}: {value}" for attr, value in self.items()]
        return "\n".join(lines)
