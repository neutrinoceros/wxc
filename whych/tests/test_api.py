import platform
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
]


def test_unexisting_package():
    name = "NotARealPackage"
    wf = WhychFinder(name)
    assert wf.module_name == name
    assert wf.path is None
    assert wf.version is None

    assert wf.get_data() == {
        "module name": name,
        "path": "unknown",
        "version": "unknown",
    }


@pytest.mark.parametrize("name", packages_sample)
def test_finder(name: str):
    pytest.importorskip(name)
    wf = WhychFinder(name)
    assert wf.module_name == name
    if platform.system() != "Windows" or not wf.assumed_stdlib:
        assert wf.path is not None
        p = Path(wf.path)
        assert p.exists()
        if not wf.assumed_stdlib:
            assert name in p.parts


@pytest.mark.parametrize("valid_query", ["path", "version", "info"])
def test_whych_wrong_query(valid_query):
    def mutate_str(s: str) -> str:
        index = random.randint(0, len(s)) - 1
        old = s[index]
        new = random.choice(ascii_lowercase.replace(old, ""))
        return s.replace(old, new, 1)

    for i in range(15):
        with pytest.raises(ValueError):
            query = mutate_str(valid_query)
            print(query)
            whych("numpy", query=query)


@pytest.mark.parametrize("name", packages_sample)
def test_info_query(name):
    res = whych(name, query="info")
    assert len(res.splitlines()) == 3
    for line in res.splitlines():
        assert (
            line.startswith("version")
            or line.startswith("path")
            or line.startswith("module name")
        )


@pytest.mark.skipif(
    platform.system() == "Windows",
    reason="On windows, can't find stdlib packages location yet",
)
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
