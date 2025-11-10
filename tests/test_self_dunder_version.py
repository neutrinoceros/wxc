from importlib.metadata import version

import pytest

import wxc


def test_dunder_version():
    assert wxc.__version__ == version("wxc")


def test_missing_attr():
    with pytest.raises(AttributeError):
        wxc.this_is_not_a_valid_member  # noqa: B018
