import json
from pathlib import Path

import pytest  # type: ignore

from pyw.api import Scope


@pytest.mark.parametrize(
    "name,except_python_version", [("math", True), ("platform", False)]
)
def test_stdlib_versions(name: str, except_python_version: bool):
    imp = Scope(name)
    assert imp["is_available"]
    assert imp["is_stdlib"]
    assert "version" in imp
    assert except_python_version is imp["version"].startswith("python")


def test_finder(a_package):
    pytest.importorskip(a_package)
    imp = Scope(a_package)
    assert imp["module_name"] == a_package
    assert "path" in imp

    p = Path(imp["path"])
    assert p.exists()
    if not imp["is_stdlib"]:
        assert a_package in p.parts


def test_get_git_hash():
    """Check that we retrieve the git hash of a package installed from a repo"""
    # pyw itself is the only repo that can reliably be used to test this
    # feature
    res = Scope("pyw")
    assert "git_hash" in res


def test_lookup_error():
    """Check that Scope._lookup internal function fails
    with LookupError in case we use it to retrieve a non-str attribute
    in an existing module.
    """
    imp = Scope("pathlib")
    with pytest.raises(LookupError):
        imp._lookup(module=json, attrs=("dump",), stdlib_default="")


def test_getline():
    imp = Scope("pathlib.Path")
    assert imp.get("line", -1) > 0

    imp = Scope("pathlib.Path.home")
    assert imp.get("line", -1) > 0
