from pathlib import Path

import pytest
from schema import Optional, Schema

from pyw.api import get_full_data

template = Schema(
    {
        "source": str,
        "in_stdlib": bool,
        Optional("version"): str,
    }
)


@pytest.mark.parametrize("name", ["NotARealPackage", "os.path.NotARealMember"])
def test_non_existing_member(name):
    data = get_full_data(name)
    assert data == {}


def test_empty_module_query(shared_datadir, monkeypatch):
    """Check for robustness of get_full_data
    with an empty module (in particular, no version data)
    """
    fake_module = shared_datadir / "fake_empty_module"
    syspath, name = fake_module.parent, fake_module.name
    monkeypatch.syspath_prepend(syspath)

    data = get_full_data(name)
    filename, _, _ = data["source"].partition(":")
    assert Path(syspath, name) in Path(filename).parents
    assert "version" not in data

    template.validate(data)


def test_field_member():
    d1 = get_full_data("os.path")
    d2 = get_full_data("os.path.expanduser")

    template.validate(d1)
    template.validate(d2)

    assert d2["version"] == d1["version"]
    assert d2["in_stdlib"] is True
    assert d1["in_stdlib"] is True


def test_compiled_stdlib_member():
    get_full_data("math.sqrt")
