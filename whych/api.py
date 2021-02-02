import inspect
import os
import sysconfig
from datetime import datetime
from importlib import import_module
from importlib.metadata import PackageNotFoundError, version as md_version
from itertools import accumulate
from pathlib import Path
from platform import python_version
from subprocess import CalledProcessError, run
from types import ModuleType
from typing import Iterable, List, Optional, Union

from .externs._stdlib_list import in_stdlib


class Importable(dict):
    def __init__(self, n: Optional[Union[str, bytes]] = None):
        if n is not None:
            self.from_name(str(n))

    def from_name(self, importable_name: str):
        parts = importable_name.split(".")

        self["package_name"] = parts[0]
        self["is_stdlib"] = in_stdlib(self["package_name"])

        idx = 0
        name_candidates = list(accumulate(parts, lambda x, y: ".".join([x, y])))
        for name in reversed(name_candidates):
            try:
                module = import_module(name)
                self["is_available"] = True
                self["member"] = ".".join(parts[idx + 1 :])
                break
            except ModuleNotFoundError:
                idx += 1
                continue
        else:
            self["is_available"] = False
            return

        self["module_name"] = module.__name__
        self["is_module"] = name == importable_name and inspect.ismodule(module)

        ver = self._lookup(
            module,
            attrs=["__version__", "VERSION"],
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
            process = run(
                ["git", "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
            )
            hash = process.stdout.decode("utf-8")
            self["git_hash"] = hash.replace("\n", "")
        except (FileNotFoundError, CalledProcessError):
            pass

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
                        f"Unexpected return value {ret=}, with type {type(ret)}"
                    )
                return ret
            except AttributeError:
                pass

        if self["is_stdlib"]:
            return stdlib_default

        return None

    def __str__(self):
        lines = [f"{attr}: {value}" for attr, value in sorted(self.items())]
        return "\n".join(lines)


def query(
    importable_names: Union[str, Iterable[str]],
    field: str = "path",
    fill_value: Optional[str] = None,
) -> List[Optional[str]]:
    if isinstance(importable_names, str):
        importable_names = [importable_names]

    res: List[Optional[str]] = []
    for name in importable_names:
        data = Importable(name)

        if field == "info":
            res.append(str(data))
            continue
        elif field == "path_and_line":
            p: Optional[str] = fill_value
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

    return res
