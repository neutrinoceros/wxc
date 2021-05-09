from pathlib import Path

import pytest  # type: ignore

from wxc.api import get_full_data


@pytest.mark.parametrize(
    "name,except_python_version", [("math", True), ("platform", False)]
)
def test_stdlib_versions(name: str, except_python_version: bool):
    imp = get_full_data(name)
    assert imp["in_stdlib"]
    assert "version" in imp
    assert except_python_version is imp["version"].startswith("Python")


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
    line1 = get_full_data("pathlib.Path")["source"].split(":")[1]
    line2 = get_full_data("pathlib.Path.chmod")["source"].split(":")[1]
    assert line1 != line2


def test_wrong_package():
    with pytest.raises(ImportError):
        get_full_data("NotARealPackage")


def test_wrong_member():
    with pytest.raises(
        AttributeError, match="os.path has no member 'NotARealMember'."
    ):
        get_full_data("os.path.NotARealMember")
