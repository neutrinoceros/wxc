from importlib import import_module
from importlib.util import find_spec

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
    # rich may output an unspecified amount of newlines
    # that don't actually affect the result visually
    assert out.strip() == ""
    assert err == "ERROR no installed package with name 'NotARealPackage'\n"


def test_stdlib_typos_in_module_name(capsys):
    res = main(["sis"])
    assert res != 0
    out, err = capsys.readouterr()
    # rich may output an unspecified amount of newlines
    # that don't actually affect the result visually
    assert out.strip() == ""
    assert err == "ERROR no installed package with name 'sis'. Did you mean 'sys' ?\n"


def test_non_existing_member(capsys):
    ret = main(["pathlib.nothing"])
    assert ret != 0
    out, err = capsys.readouterr()
    # rich may output an unspecified amount of newlines
    # that don't actually affect the result visually
    assert out.strip() == ""

    assert err.startswith("ERROR module 'pathlib' has no attribute 'nothing'")


def test_compiled_source(capsys):
    pytest.importorskip("Cython")
    ret = main(["Cython.Compiler.Code.IntConst"])
    out, err = capsys.readouterr()
    assert err == (
        "ERROR failed to locate source data. 'Cython.Compiler.Code.IntConst' "
        "is a C-compiled function.\n"
    )
    # rich may output an unspecified amount of newlines
    # that don't actually affect the result visually
    assert out.strip() == ""
    assert ret != 0


def test_typo1(capsys):
    ret = main(["pathlib.Path.chmode"])
    out, err = capsys.readouterr()
    assert err.startswith(
        "ERROR type object 'pathlib.Path' has no attribute 'chmode'. "
        "Here are close matches:\n"
    )
    # rich may output an unspecified amount of newlines
    # that don't actually affect the result visually
    assert out.strip() == ""
    assert ret != 0


def test_typo2(capsys):
    ret = main(["pathlib.Path.homme"])
    out, err = capsys.readouterr()
    assert (
        err
        == "ERROR type object 'pathlib.Path' has no attribute 'homme'. Did you mean 'home' ?\n"
    )
    # rich may output an unspecified amount of newlines
    # that don't actually affect the result visually
    assert out.strip() == ""
    assert ret != 0


@pytest.mark.skipif(
    find_spec("importlib_metadata") is None,
    reason="importlib_metadata isn't a hard dependency",
)
def test_normalize_hyphen(capsys):
    # note that use a simple pytest.mark.skipif instead of pytest.importorskip
    # because the latter doesn't seem to play nice with coverage
    ret = main(["importlib-metadata"])
    out, err = capsys.readouterr()
    assert err == ""
    assert out
    assert ret == 0


def test_source(fake_module, capsys):
    expected = (
        """\n"""
        """  4 def import_me_if_you_can():\n"""
        '''  5     """Docstrings are good. Use them."""\n'''
        """  6     return "Gotcha"\n"""
        """  7 \n"""
    )
    syspath, name = fake_module
    ret = main([f"{name}.import_me_if_you_can", "--source", "--lines"])
    out, err = capsys.readouterr()
    assert out.startswith(expected)
    assert err == ""
    assert ret == 0


def test_source_error(capsys):
    pytest.importorskip("Cython")
    ret1 = main(["Cython.array"])
    assert ret1 == 0
    out, err = capsys.readouterr()
    assert out != ""
    assert err == ""

    ret2 = main(["Cython.array", "-s"])
    out, err = capsys.readouterr()
    # rich may output an unspecified amount of newlines
    # that don't actually affect the result visually
    assert out.strip() == ""
    # the exact error message varies depending on the Python runtime, which is fine
    assert err.startswith("ERROR")
    assert ret2 != 0


def test_lines_no_source(capsys):
    ret1 = main(["inspect.getfile", "--lines"])
    assert ret1 != 0
    out, err = capsys.readouterr()
    assert out == ""
    assert err == "ERROR --lines flag is meaningless if --source isn't passed too\n"


def test_property(capsys):
    ret = main(["rich.progress.Task.started"])
    assert ret == 0
    out, err = capsys.readouterr()
    assert out != ""
    assert err == ""
