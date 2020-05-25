import json
import random
from importlib import import_module
from pathlib import Path
from string import ascii_lowercase

import pytest  # type: ignore

from whych.api import WhychFinder, whych

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


def test_recycle_finder():
    wf = WhychFinder("math")
    d1 = wf.get_data()
    wf.module_name = "platform"
    d2 = wf.get_data()
    keys = list(d1.keys())
    keys.remove("stdlib")
    for k in keys:
        assert d2[k] != d1[k]


@pytest.mark.parametrize(
    "name,except_python_version", [("math", True), ("platform", False)]
)
def test_stdlib_versions(name: str, except_python_version: bool):
    wf = WhychFinder(name)
    assert wf.in_stdlib()
    assert wf.version is not None
    assert except_python_version is wf.version.startswith("python")


def test_unexisting_package():
    name = "NotARealPackage"
    wf = WhychFinder(name)
    assert wf.module_name == name
    assert wf.path is None
    assert wf.version is None

    expected = {
        "module name": name,
        "path": "unknown",
        "version": "unknown",
        "stdlib": False,
    }
    actual = wf.get_data()
    for k, v in expected.items():
        assert actual[k] == v


@pytest.mark.parametrize("name", packages_sample)
def test_finder(name: str):
    pytest.importorskip(name)
    wf = WhychFinder(name)
    assert wf.module_name == name
    assert wf.path is not None
    p = Path(wf.path)
    assert p.exists()
    if not wf.in_stdlib():
        assert name in p.parts


@pytest.mark.parametrize("valid_query", ["path", "version", "info"])
def test_whych_wrong_query(valid_query):
    def mutate_str(s: str) -> str:
        index = random.randint(0, len(s)) - 1
        old = s[index]
        new = random.choice(ascii_lowercase.replace(old, ""))
        return s.replace(old, new, 1)

    for _ in range(15):
        with pytest.raises(ValueError):
            query = mutate_str(valid_query)
            print(query)
            whych("numpy", query=query)


@pytest.mark.parametrize("name", packages_sample)
def test_info_query(name, tmp_path):
    res = whych(name, query="info")
    with open(tmp_path / "package_data.json", mode="wt") as fileobj:
        json.dump(res, fileobj)


@pytest.mark.parametrize("name", packages_sample + ["NotARealPackage"])
def test_elementary_queries(name):
    version = whych(name, query="version")
    path = whych(name, query="version")
    try:
        import_module(name)
        assert version != "unknown"
        assert path != "unknown"

    except ImportError:
        assert version == "unknown"
        assert path == "unknown"
