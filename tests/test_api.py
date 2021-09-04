import sys
from pathlib import Path

import pytest  # type: ignore

from wxc.api import get_full_data


@pytest.mark.skipif(
    sys.platform.startswith("win"),
    reason="On Windows, we can't even locate these files",
)
@pytest.mark.parametrize(
    "name,except_python_version", [("math", True), ("platform", False)]
)
def test_stdlib_versions(name: str, except_python_version: bool):
    imp = get_full_data(name)
    assert imp["in_stdlib"]
    assert "version" in imp
    assert except_python_version is imp["version"].startswith("Python")


@pytest.mark.skipif(
    sys.platform.startswith("win"),
    reason="parsing is more convoluted when ':' is a normal path element",
)
def test_finder(package_name):
    pytest.importorskip(package_name)
    imp = get_full_data(package_name)
    assert "source" in imp

    filename, _, line = imp["source"].partition(":")
    p = Path(filename)
    assert p.exists()
    if not imp["in_stdlib"]:
        assert package_name in p.parts


def test_get_obj():
    line1 = get_full_data("pathlib.Path")["source"].partition(":")[-1]
    line2 = get_full_data("pathlib.Path.chmod")["source"].partition(":")[-1]
    assert line1 != ""
    assert line2 != ""
    assert line1 != line2


def test_wrong_package():
    with pytest.raises(ImportError):
        get_full_data("NotARealPackage")


def test_wrong_member():
    with pytest.raises(
        AttributeError,
        match="module 'os.path' has no attribute 'NotARealMember'",
    ):
        get_full_data("os.path.NotARealMember")
