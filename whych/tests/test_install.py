import os
import sys
import tempfile

import pytest

from whych._installer import _lookup_rcfile, main


@pytest.mark.skipif(sys.platform.startswith("win"), reason="no windows support")
def test_lookup_rcfile():
    rcfile = _lookup_rcfile(interactive=False)
    assert rcfile.is_file()


@pytest.mark.skipif(sys.platform.startswith("win"), reason="no windows support")
def test_install():
    with tempfile.TemporaryDirectory() as tmpdir:
        main(install_dir=os.path.join(tmpdir, ".app"))
