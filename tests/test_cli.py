from importlib import import_module

import pytest

from pyw.cli import main

valid_queries = [None, "--version", "-v", "--full", "-f"]


@pytest.mark.parametrize("arg", valid_queries)
def test_query_valid_field(arg):
    argv = ["os.path.join"]
    if arg is not None:
        argv.append(arg)
    main(argv)


def test_elementary_queries(capsys, package_name):

    try:
        import_module(package_name)
    except ImportError:
        pytest.skip()

    res = main([package_name, "--version"])
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
    assert err == "Error: did not resolve any data for 'NotARealPackage'\n"


def test_non_existing_member(capsys):
    ret = main(["pathlib.lol"])
    assert ret != 0
    out, err = capsys.readouterr()
    assert out == ""
    assert err == "Error: did not resolve any data for 'pathlib.lol'\n"
