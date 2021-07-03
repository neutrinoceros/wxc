import pytest

from wxc.api import get_obj
from wxc.cli import main

BUILTINS_TO_CHECK = frozenset(
    (
        "print",
        "object",
    )
)


@pytest.mark.parametrize("name", BUILTINS_TO_CHECK)
def test_inspect_builtin(name):
    # check that this doesn't fail brutally
    get_obj(name)


@pytest.mark.parametrize("name", BUILTINS_TO_CHECK)
def test_fail_builtins(name, capsys):
    ret = main([name])

    out, err = capsys.readouterr()
    assert out == ""
    assert err == (
        "Error: failed to locate source data. "
        f"'{name}' is a builtin object.\n"
    )
    assert ret != 0
