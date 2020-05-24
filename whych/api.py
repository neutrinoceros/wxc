import sysconfig
from importlib import import_module
from platform import python_version
from typing import Union

from stdlib_list import in_stdlib


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

    if query in ("version", "path"):
        attr = getattr(finder, query)
        if attr is None:
            return "unknown"
        else:
            return str(attr)
    else:
        raise ValueError(f"Unsupported query type '{query}'.")
