import sys

import pytest


@pytest.fixture(params=(True, False))
def has_importlib_metadata(request, monkeypatch):
    if not request.param:
        monkeypatch.setitem(sys.modules, "importlib.metadata", None)
    return request.param


def test_foo(has_importlib_metadata):
    from whych.cli import main

    res = main(["os.path.join"])
    assert res == 0
