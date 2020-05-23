from importlib import import_module
from sys import version as sysversion

from typing import Union


class WhychFinder:
    module = None
    _version = None
    _path = None

    def __init__(self, module_name: str):
        self.module_name = module_name
        try:
            self.module = import_module(module_name)
        except ModuleNotFoundError:
            pass

    @property
    def version(self) -> Union[str, None]:
        for attr in ("__version__", "VERSION"):
            try:
                self._version = getattr(self.module, attr)
            except AttributeError:
                pass

        if (
            self._version is None
            and self.path is not None
            and "site-package" not in self.path
        ):
            self._version = sysversion

        return self._version

    @property
    def path(self) -> Union[str, None]:
        if self.module is not None:
            self._path = self.module.__file__
        return self._path

    def get_data(self) -> dict:
        data = {
            "module name": self.module_name,
            "path": self.path,
            "version": self.version,
        }
        data.update({k: v or "unknown" for k, v in data.items()})
        return data


def whych(module_name: str, query: str = "path") -> str:
    finder = WhychFinder(module_name)

    if query == "info":
        data = finder.get_data()
        lines = [f"{attr}: {value}" for attr, value in data.items()]
        return "\n".join(lines)

    if query == "version":
        return finder.version or "unknown"

    return finder.path
