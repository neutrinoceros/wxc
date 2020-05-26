import json
import os
import platform
import random
from importlib import import_module
from pathlib import Path
from string import ascii_lowercase

import pytest  # type: ignore

from whych.api import Importable, get_data, query

packages_sample = [
    # stdlib
    "math",
    "platform",
    "uuid",
    "fraction",
    # common third party
    "numpy",
    "matplotlib",
    "pandas",
    "requests",
    "django",
    "flask",
    "IPython",
    "tqdm",
    "toml",
]

fake_empty_module = (Path(__file__).parent / "data", "fake_empty_module")
fake_versioned_module_path = (
    Path(__file__).parent / "data",
    "fake_versioned_module",
)


@pytest.mark.parametrize(
    "name,except_python_version", [("math", True), ("platform", False)]
)
def test_stdlib_versions(name: str, except_python_version: bool):
    imp = Importable(name)
    assert imp.is_found
    assert imp.is_stdlib
    assert imp.version is not None
    assert except_python_version is imp.version.startswith("python")


@pytest.mark.parametrize("name", ["NotARealPackage", "os.path.NotARealMember"])
def test_unexisting_member(name):
    imp = Importable(name)
    assert imp.module_name is None
    assert imp.path is None
    assert imp.version is None

    expected = {
        "module name": "unknown",
        "path": "unknown",
        "version": "unknown",
        "stdlib": False,
    }
    actual = get_data(name)
    for k, v in expected.items():
        assert actual[k] == v


@pytest.mark.parametrize("name", packages_sample)
def test_finder(name: str):
    pytest.importorskip(name)
    imp = Importable(name)
    assert imp.module_name == name
    assert imp.path is not None
    p = Path(imp.path)
    assert p.exists()
    if not imp.is_stdlib:
        assert name in p.parts


@pytest.mark.parametrize("valid_field", ["path", "version", "info"])
def test_query_wrong_field(valid_field):
    def mutate_str(s: str) -> str:
        index = random.randint(0, len(s)) - 1
        old = s[index]
        new = random.choice(ascii_lowercase.replace(old, ""))
        return s.replace(old, new, 1)

    for _ in range(15):
        with pytest.raises(ValueError):
            field = mutate_str(valid_field)
            query("numpy", field=field)


@pytest.mark.parametrize("name", packages_sample)
def test_info_field(name, tmp_path):
    res = query(name, field="info")
    with open(tmp_path / "package_data.json", mode="wt") as fileobj:
        json.dump(res, fileobj)


@pytest.mark.parametrize("name", packages_sample + ["NotARealPackage"])
def test_elementary_queries(name):
    version = query(name, field="version")
    path = query(name, field="version")
    try:
        import_module(name)
        assert version != "unknown"
        assert path != "unknown"

    except ImportError:
        assert version == "unknown"
        assert path == "unknown"


def test_empty_module_finder(monkeypatch):
    """Check for robustness of WhichFinder.get_data()
    with an empty module (in particular, no version data)
    """
    syspath, name = fake_empty_module
    monkeypatch.syspath_prepend(syspath)

    data = get_data(name)
    assert data["path"] == os.path.join(syspath, name)
    assert data["version"] == "unknown"


def test_muliple_packages():
    res = query(["math", "platform", "numpy"])
    assert len(res) == 3


def test_field_member():
    d1 = get_data("os.path")
    d2 = get_data("os.path.expanduser")

    if platform.system() != "Windows":
        assert d2["module name"] == d1["module name"] == "posixpath"
    assert d2["version"] == d1["version"]
    assert d2["stdlib"] is d1["stdlib"] is True
