import os
import sysconfig
from datetime import datetime
from importlib import import_module
from platform import python_version
from typing import Dict, Iterable, List, Union

from stdlib_list import in_stdlib  # type: ignore


class Importable:
    _module = None
    module_name: str = None
    path: str = None
    is_found: bool = False
    is_stdlib: bool = False

    def __init__(self, importable_name: str):
        parts = importable_name.split(".")
        self.member = parts.pop()
        if parts:
            module_name = ".".join(parts)
        else:
            module_name = self.member

        try:
            self._module = import_module(module_name)
            self.module_name = module_name
            self.is_found = True
        except ImportError:
            pass

        if self.is_found:
            self.is_stdlib = in_stdlib(self.module_name)

            self.version = self._lookup(
                attrs=("__version__", "VERSION"),
                stdlib_default=f"python {python_version()}",
            )
            self.path = self._lookup(
                attrs=("__path__", "__file__"),
                stdlib_default=sysconfig.get_paths()["stdlib"],
            )
            # additional sanitizing (sometimes useful on Windows)
            if isinstance(self.path, list):
                self.path = self.path[0]

            ts = int(os.path.getmtime(self.path))
            self.last_updated = datetime.utcfromtimestamp(ts).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

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


def get_data(
    importable_name: str, fill_value="unknown"
) -> Dict[str, Union[str, bool]]:
    imp = Importable(importable_name)

    data = {
        "module name": imp.module_name,
        "path": imp.path,
        "version": imp.version,
        "last updated": imp.last_updated,
        "stdlib": imp.in_stdlib,
    }

    data.update(
        {k: v if v is not None else fill_value for k, v in data.items()}
    )
    return data  # type: ignore


def whych(
    importable_names: Union[str, Iterable[str]], query: str = "path"
) -> Union[str, List[str]]:
    if isinstance(importable_names, str):
        importable_names = [importable_names]

    res = []
    for name in importable_names:
        data = get_data(name)

        if query == "info":
            lines = [f"{attr}: {value}" for attr, value in data.items()]
            res.append("\n".join(lines))
            continue
        try:
            res.append(str(data[query]))
        except KeyError:
            raise ValueError(f"Unsupported query type '{query}'.")
    if len(res) == 1:
        return res[0]
    return res
