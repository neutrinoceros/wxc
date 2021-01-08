import json
import random
from importlib import import_module
from pathlib import Path
from string import ascii_lowercase

import pytest  # type: ignore

from whych.api import Importable, query

packages_sample = [
    # stdlib
    "math",
    "platform",
    "uuid",
    "fractions",
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


@pytest.mark.parametrize(
    "name,except_python_version", [("math", True), ("platform", False)]
)
def test_stdlib_versions(name: str, except_python_version: bool):
    imp = Importable(name)
    assert imp["is_available"]
    assert imp["is_stdlib"]
    assert "version" in imp
    assert except_python_version is imp["version"].startswith("python")


@pytest.mark.parametrize("name", packages_sample)
def test_finder(name: str):
    pytest.importorskip(name)
    imp = Importable(name)
    assert imp["module_name"] == name
    assert "path" in imp

    p = Path(imp["path"])
    assert p.exists()
    if not imp["is_stdlib"]:
        assert name in p.parts


known_valid_query_fields = ["path", "version", "info", "path_and_line"]


@pytest.mark.parametrize("valid_field", known_valid_query_fields)
def test_query_valid_field(valid_field):
    query("os", field=valid_field)
    query("os.path.join", field=valid_field)


@pytest.mark.parametrize("valid_field", known_valid_query_fields)
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

    try:
        import_module(name)
    except ImportError:
        pytest.skip()

    query(name, field="version")


def test_muliple_packages():
    res = query(["math", "platform", "uuid"])
    assert len(res) == 3


def test_get_git_hash():
    """Check that we retrieve the git hash of a package installed from a repo"""
    # whych itself is the only repo that can reliably be used to test this
    # feature
    res = Importable("whych")
    assert "git_hash" in res


def test_lookup_error():
    """Check that Importable._lookup internal function fails
    with LookupError in case we use it to retrieve a non-str attribute
    in an existing module.
    """
    imp = Importable("pathlib")
    with pytest.raises(LookupError):
        imp._lookup(module=json, attrs=("dump",), stdlib_default="")
