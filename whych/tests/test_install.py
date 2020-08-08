import os
import tempfile

from whych._installer import _lookup_rcfile, main


def test_lookup_rcfile():
    rcfile = _lookup_rcfile(interactive=False)
    assert rcfile.is_file()


def test_install():
    with tempfile.TemporaryDirectory() as tmpdir:
        main(install_dir=os.path.join(tmpdir, ".app"))
