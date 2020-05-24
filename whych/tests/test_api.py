import random
from pathlib import Path
from string import ascii_lowercase

import pytest  # type: ignore

from whych.api import WhychFinder, whych


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


@pytest.mark.parametrize(
    "name",
    [
        "math",
        "fraction",
        "numpy",
        "matplotlib",
        "pandas",
        "requests",
        "django",
        "flask",
        "IPython",
        "tqdm",
    ],
)
def test_finder(name: str):
    pytest.importorskip(name)
    wf = WhychFinder(name)
    assert wf.module_name == name
    assert isinstance(wf.path, str)
    p = Path(wf.path)
    assert p.is_file()
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
