import inspect
import os
import sysconfig
from datetime import datetime
from importlib import import_module
from platform import python_version
from typing import Any, Dict, Iterable, List, Union

from .externs._stdlib_list import in_stdlib


class Importable:
    _module = None
    package_name: Union[str, None] = None
    module_name: Union[str, None] = None
    path: Union[str, None] = None
    version: Union[str, None] = None
    last_updated: Union[str, None] = None
    is_found: bool = False
    is_stdlib: Union[bool, None] = None
    _member: Any = None
    line: Union[int, None] = None
    is_module: bool = False

    def __init__(self, importable_name: str):
        parts = importable_name.split(".")
        self.member = parts[-1]
        names_to_try = [importable_name]
        if parts:
            names_to_try.append(".".join(parts[:-1]))

        for name in names_to_try:
            try:
                module = import_module(name)
                if name == importable_name:
                    self._member = module
                else:
                    self._member = getattr(module, self.member)
                self.is_module = inspect.ismodule(self._member)
                self._module = module
                self.package_name = parts[0]
                self.module_name = module.__name__
                self.is_found = True
                break
            except (ModuleNotFoundError, ValueError, AttributeError):
                pass

        if self.is_found:

            self.is_stdlib = in_stdlib(self.package_name)

            self.version = self._lookup(
                attrs=("__version__", "VERSION"),
                stdlib_default=f"python {python_version()}",
            )
            self.path = self.resolve_path()
            try:
                self.line = inspect.getsourcelines(self._member)[1]
            except (TypeError, OSError):
                pass

            if isinstance(self.path, str):
                ts = int(os.path.getmtime(self.path))
                self.last_updated = datetime.utcfromtimestamp(ts).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

    def resolve_path(self):
        try:
            return inspect.getabsfile(self._member)
        except TypeError:
            path = self._lookup(
                attrs=("__file__", "__path__"),
                stdlib_default=sysconfig.get_paths()["stdlib"],
            )
            # additional sanitizing (sometimes useful on Windows)
            if isinstance(path, list):
                return path[0]
            return path

    def _lookup(
        self, attrs: Iterable[str], stdlib_default: str
    ) -> Union[str, None]:

        for attr in attrs:
            try:
                return getattr(self._module, attr)
            except AttributeError:
                pass

        if self.is_stdlib:
            return stdlib_default

        return None


def get_data(importable_name: str, fill_value=None) -> Dict[str, Any]:
    imp = Importable(importable_name)

    data = {
        "module name": imp.module_name,
        "path": imp.path,
        "version": imp.version,
        "last updated": imp.last_updated,
        "stdlib": imp.is_stdlib,
        "line": imp.line,
        "is a module": imp.is_module,
        "found": imp.is_found,
    }

    data.update(
        {k: v if v is not None else fill_value for k, v in data.items()}
    )
    return data  # type: ignore


def query(
    importable_names: Union[str, Iterable[str]],
    field: str = "path",
    fill_value: Any = None,
) -> Union[Any, List[Any]]:
    if isinstance(importable_names, str):
        importable_names = [importable_names]

    res = []
    for name in importable_names:
        data = get_data(name)

        if field == "info":
            lines = [f"{attr}: {value}" for attr, value in data.items()]
            res.append("\n".join(lines))
            continue
        elif field == "path_and_line":
            p: Any = fill_value
            if data["found"]:
                p = str(data["path"])
                if not data["is a module"]:
                    p += f":{data['line']}"

            res.append(p)
            continue
        try:
            res.append(data[field])
        except KeyError:
            raise ValueError(f"Unsupported query type '{field}'.")
    if len(res) == 1:
        return res[0]
    return res
