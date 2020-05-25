import os
import sysconfig
from datetime import datetime
from importlib import import_module
from platform import python_version
from typing import Dict, Union

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

    @property
    def version(self) -> Union[str, None]:
        for attr in ("__version__", "VERSION"):
            try:
                self._version = getattr(self.module, attr)
                break
            except AttributeError:
                pass
        else:
            if self.in_stdlib():
                self._version = f"python {python_version()}"

        return self._version

    @property
    def path(self) -> Union[str, None]:
        if self.module is not None:
            for attr in ("__path__", "__file__"):
                try:
                    self._path = getattr(self.module, attr)
                    break
                except AttributeError:
                    pass
            else:
                if self.in_stdlib():
                    self._path = sysconfig.get_paths()["stdlib"]
        if isinstance(self._path, list):
            self._path = self._path[0]
        return self._path

    def in_stdlib(self):
        return in_stdlib(self.module_name)

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


def whych(module_name: str, query: str = "path") -> str:
    finder = WhychFinder(module_name)
    data = finder.get_data()

    if query == "info":
        lines = [f"{attr}: {value}" for attr, value in data.items()]
        return "\n".join(lines)

    try:
        return str(data[query])
    except KeyError:
        raise ValueError(f"Unsupported query type '{query}'.")
