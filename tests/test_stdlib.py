import pytest

from wxc.api import get_obj, get_sourcefile
from wxc.cli import main

TO_CHECK = frozenset(("os.fspath", "math.sqrt"))


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
    # rich may output an unspecified amount of newlines
    # that don't actually affect the result visually
    assert out.strip() == ""
    assert (
        err
        == f"ERROR failed to locate source data. {name!r} is a C-compiled function.\n"
    )
    assert ret != 0
