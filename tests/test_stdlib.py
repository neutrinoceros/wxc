import sys

import pytest

from wxc.api import get_obj, get_sourcefile
from wxc.cli import main

TO_CHECK = frozenset(("os.fspath", "math.sqrt"))


@pytest.mark.skipif(
    sys.version_info < (3, 7),
    reason="This error message was changed in Python 3.7",
)
@pytest.mark.parametrize("name", TO_CHECK)
def test_get_data_builtin(name):
    obj = get_obj(name)
    with pytest.raises(
        TypeError,
        match=(
            r"module, class, method, function, traceback, frame, or code object was expected,"
            " got builtin_function_or_method"
        ),
    ):
        get_sourcefile(obj)


@pytest.mark.parametrize("name", TO_CHECK)
def test_cli_builtin(name, capsys):
    ret = main([name])
    out, err = capsys.readouterr()
    assert out == ""
    assert (
        err
        == f"Error: failed to locate source data. {name!r} is a builtin function.\n"
    )
    assert ret != 0
