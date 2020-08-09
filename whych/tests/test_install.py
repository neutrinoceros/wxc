import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest
from whych import _installer
from whych._installer import _lookup_rcfile, main


@pytest.mark.skipif(sys.platform.startswith("win"), reason="no windows support")
def test_lookup_rcfile():
    rcfile = _lookup_rcfile(interactive=False)
    assert rcfile.is_file()


@pytest.mark.skipif(sys.platform.startswith("win"), reason="no windows support")
def test_install():

    with tempfile.TemporaryDirectory() as tmpdir:
        with tempfile.NamedTemporaryFile(dir=str(Path.home())) as tmprcfile:
            with mock.patch.object(
                _installer, "RCFILE_LOOKUP_TABLE", [tmprcfile.name]
            ):
                install_dir = os.path.join(tmpdir, ".app")
                main(install_dir=install_dir)
                with pytest.raises(SystemExit):
                    main(install_dir=install_dir)
