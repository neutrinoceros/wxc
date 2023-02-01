import sys
from pathlib import Path

import pytest
from schema import Optional, Schema

from wxc.api import get_full_data

template = Schema(
    {
        "source": str,
        "in_stdlib": bool,
        Optional("version"): str,
    }
)


@pytest.mark.skipif(
    sys.platform.startswith("win"),
    reason="parsing is more convoluted when ':' is a normal path element",
)
def test_empty_module_query(fake_module):
    """Check for robustness of get_full_data
    with an empty module (in particular, no version data)
    """
    syspath, name = fake_module
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
