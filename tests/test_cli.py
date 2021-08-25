import sys
from importlib import import_module

import pytest

from wxc.cli import main

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

    ret = main([package_name, "--version"])

    out, err = capsys.readouterr()

    if package_name == "math" and sys.platform.startswith("win"):
        assert out == ""
        assert err == "Error: failed to locate source data.\n"
        assert ret != 0
        return

    assert out != "unknown"
    assert err == ""
    assert ret == 0


@pytest.mark.parametrize("arg", valid_queries)
def test_falty_queries(capsys, arg):
    argv = ["NotARealPackage"]
    if arg is not None:
        argv.append(arg)
    res = main(argv)
    assert res != 0
    out, err = capsys.readouterr()
    assert out == ""
    assert err == "Error: no installed package with name 'NotARealPackage'\n"


@pytest.mark.skipif(
    sys.version_info < (3, 10),
    reason="this feature is reserved to Python 3.10 and newer",
)
def test_stdlib_typos_in_module_name(capsys):
    res = main(["sis"])
    assert res != 0
    out, err = capsys.readouterr()
    assert out == ""
    assert (
        err
        == "Error: no installed package with name 'sis'. Did you mean 'sys' ?\n"
    )


def test_non_existing_member(capsys):
    ret = main(["pathlib.nothing"])
    assert ret != 0
    out, err = capsys.readouterr()
    assert out == ""
    assert (
        # not matching exact results since they are different between Python 3.9 and 3.10
        err.startswith(
            "Error: module 'pathlib' has no attribute 'nothing'."
            " Here are the closest matches:"
        )
    )


def test_compiled_source(capsys):
    pytest.importorskip("numpy")
    ret = main(["numpy.abs"])
    out, err = capsys.readouterr()
    assert err == "Error: did not resolve source file for 'numpy.abs'\n"
    assert out == ""
    assert ret != 0


def test_typo1(capsys):
    ret = main(["pathlib.Path.chmode"])
    out, err = capsys.readouterr()
    assert (
        err
        == "Error: type object 'pathlib.Path' has no attribute 'chmode'. Did you mean 'chmod' ?\n"
    )
    assert out == ""
    assert ret != 0


def test_typo2(capsys):
    ret = main(["pathlib.Path.homme"])
    out, err = capsys.readouterr()
    assert (
        err
        == "Error: type object 'pathlib.Path' has no attribute 'homme'. Did you mean 'home' ?\n"
    )
    assert out == ""
    assert ret != 0


def test_normalize_hyphen(capsys):
    pytest.importorskip("matplotlib_inline")
    ret = main(["matplotlib-inline"])
    out, err = capsys.readouterr()
    assert err == ""
    assert out
    assert ret == 0


def test_source(fake_module, capsys):

    expected = (
        """  4 def import_me_if_you_can():\n"""
        '''  5     """Docstrings are good. Use them."""\n'''
        """  6     return "Gotcha"\n"""
        """  7 \n"""
    )
    syspath, name = fake_module
    ret = main([f"{name}.import_me_if_you_can", "--source"])
    out, err = capsys.readouterr()
    assert out.startswith(expected)
    assert err == ""
    assert ret == 0
