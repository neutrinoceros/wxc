import inspect
import os
import sysconfig
from datetime import datetime
from importlib import import_module
from importlib.metadata import PackageNotFoundError, version as md_version
from pathlib import Path
from platform import python_version
from subprocess import CalledProcessError, run
from typing import Any, Iterable, List, Union

from .externs._stdlib_list import in_stdlib


class Importable(dict):
    def __init__(self, n=None):
        if isinstance(n, (str, bytes)):
            self.from_name(n)

    def from_name(self, importable_name: str):
        parts = importable_name.split(".")

        names = [importable_name]
        if len(parts) > 1:
            names.append(".".join(parts[:-1]))
        self["package_name"] = parts[0]
        self["member"] = parts[-1]
        self["is_stdlib"] = in_stdlib(self["package_name"])

        module = None
        for name in names:
            try:
                module = import_module(name)
                break
            except ModuleNotFoundError:
                continue

        self["is_available"] = module is not None

        if not self["is_available"]:
            return

        self["module_name"] = module.__name__
        self["is_module"] = name == importable_name and inspect.ismodule(module)

        ver = self._lookup(
            module,
            attrs=("__version__", "VERSION"),
            stdlib_default=f"python {python_version()}",
        )
        if ver is None:
            try:
                ver = md_version(self["package_name"])
            except PackageNotFoundError:
                pass
        if ver:
            self["version"] = ver

        self["path"] = self.resolve_path(module)
        try:
            self["line"] = inspect.getsourcelines(module)[1]
        except (TypeError, OSError):
            pass

        ts = int(os.path.getmtime(self["path"]))
        self["last_updated"] = datetime.utcfromtimestamp(ts).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        try:
            os.chdir(Path(self["path"]).parent)
            process = run(
                ["git", "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
            )
            hash = process.stdout.decode("utf-8")
            self["git_hash"] = hash.replace("\n", "")
        except (FileNotFoundError, CalledProcessError):
            pass

    def resolve_path(self, module):
        try:
            return inspect.getabsfile(self["member"])
        except TypeError:
            path = self._lookup(
                module,
                attrs=("__file__", "__path__"),
                stdlib_default=sysconfig.get_paths()["stdlib"],
            )
            return path

    def _lookup(
        self, module: Any, attrs: Iterable[str], stdlib_default: str
    ) -> Union[str, None]:

        for attr in attrs:
            try:
                return getattr(module, attr)
            except AttributeError:
                pass

        if self["is_stdlib"]:
            return stdlib_default

        return None

    def __str__(self):
        lines = [f"{attr}: {value}" for attr, value in self.items()]
        return "\n".join(lines)


def query(
    importable_names: Union[str, Iterable[str]],
    field: str = "path",
    fill_value: Any = None,
) -> Union[Any, List[Any]]:
    if isinstance(importable_names, str):
        importable_names = [importable_names]

    res = []
    for name in importable_names:
        data = Importable(name)

        if field == "info":
            res.append(str(data))
            continue
        elif field == "path_and_line":
            p: Any = fill_value
            if data["is_available"]:
                p = str(data["path"])
                if not data["is_module"]:
                    p += f":{data['line']}"

            res.append(p)
            continue
        try:
            res.append(data[field])
        except KeyError as err:
            raise ValueError(f"Could not determine field `{field}`.") from err
    if len(res) == 1:
        return res[0]
    return res
