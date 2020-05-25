import os
import sysconfig
from datetime import datetime
from importlib import import_module
from platform import python_version
from typing import Dict, Iterable, List, Union

from stdlib_list import in_stdlib  # type: ignore


class WhychFinder:
    module = None
    _module_name = None
    _version = None
    _path = None
    _last_updated = None

    def __init__(self, module_name: str = None):
        self.module_name = module_name

    @property
    def module_name(self):
        return self._module_name

    @module_name.setter
    def module_name(self, new: str):
        self._module_name = new
        if new is not None:
            try:
                self.module = import_module(new)
            except ModuleNotFoundError:
                self.module = None

    def in_stdlib(self):
        return in_stdlib(self.module_name)

    def _lookup(
        self, attrs: Iterable[str], stdlib_default: str
    ) -> Union[str, None]:

        for attr in attrs:
            try:
                return getattr(self.module, attr)
            except AttributeError:
                pass

        if self.in_stdlib():
            return stdlib_default

        return None

    @property
    def version(self) -> Union[str, None]:
        self._version = self._lookup(
            attrs=("__version__", "VERSION"),
            stdlib_default=f"python {python_version()}",
        )
        return self._version

    @property
    def path(self) -> Union[str, None]:
        self._path = self._lookup(
            attrs=("__path__", "__file__"),
            stdlib_default=sysconfig.get_paths()["stdlib"],
        )
        # additional sanitizing (sometimes useful on Windows)
        if isinstance(self._path, list):
            self._path = self._path[0]
        return self._path

    @property
    def last_updated(self):
        if self.path is not None:
            ts = int(os.path.getmtime(self.path))
            self._last_updated = datetime.utcfromtimestamp(ts).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        return self._last_updated

    def get_data(self, module_name: str = None) -> Dict[str, Union[str, bool]]:
        if module_name is not None:
            self.module_name = module_name
        elif self._module_name is None:
            raise RuntimeError

        data = {
            "module name": self.module_name,
            "path": self.path,
            "version": self.version,
            "last updated": self.last_updated,
            "stdlib": self.in_stdlib(),
        }

        data.update(
            {k: v if v is not None else "unknown" for k, v in data.items()}
        )
        return data  # type: ignore


def whych(
    module_name: Union[str, Iterable[str]], query: str = "path"
) -> Union[str, List[str]]:
    finder = WhychFinder()
    if isinstance(module_name, str):
        module_name = [module_name]

    res = []
    for name in module_name:
        data = finder.get_data(name)

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
