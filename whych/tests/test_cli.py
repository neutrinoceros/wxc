from importlib import import_module

import pytest

from whych.cli import main

valid_queries = [None, "--version", "--info", "--json"]


@pytest.mark.parametrize("arg", valid_queries)
def test_query_valid_field(arg):
    argv = ["os.path.join"]
    if arg is not None:
        argv.append(arg)
    main(argv)


def test_elementary_queries(capsys, a_package):

    try:
        import_module(a_package)
    except ImportError:
        pytest.skip()

    res = main([a_package, "--version"])
    assert res == 0

    out, err = capsys.readouterr()
    assert out != "unknown"
    assert err == ""


@pytest.mark.parametrize("arg", valid_queries)
def test_falty_queries(capsys, arg):
    argv = ["NotARealPackage"]
    if arg is not None:
        argv.append(arg)
    res = main(argv)
    assert res != 0
    out, err = capsys.readouterr()
    assert out == ""
    assert err.startswith("unknown")
