import os
import stat
import sys
from pathlib import Path

RCFILE_LOOKUP_TABLE = [".zshrc", ".bashrc", ".bash_profile"]
THIS_FILE = Path(__file__).resolve()
REPO_DIR = THIS_FILE.parents[1]
DEFAULT_INSTALL_DIR = REPO_DIR / ".app"


def _lookup_rcfile(interactive: bool):

    found = [
        file for file in RCFILE_LOOKUP_TABLE if (Path.home() / file).is_file()
    ]
    if not found:
        raise FileNotFoundError(
            "Could not determine your shell configuration file"
        )

    if interactive and len(found) > 1:
        filename = ""
        while filename not in found:
            filename = input(
                "Please select your shell configuration file "
                f"({', '.join(found)}))    "
            )
    else:
        filename = found[0]

    rcfile = Path.home() / filename
    return rcfile


def main(install_dir=None, rcfile=None):

    if install_dir is None:
        install_dir = DEFAULT_INSTALL_DIR
    install_dir = Path(install_dir)

    try:
        install_dir.mkdir()
    except FileExistsError:
        print(
            f"{install_dir} already exists. "
            "Please remove this directory before installing again. "
            "You might also need to cleanup your shell rc file."
        )
        sys.exit(1)

    # create an executable symlink
    app_file = install_dir / "pyw"
    app_file.symlink_to(REPO_DIR.joinpath("pyw", "__main__.py"))
    st = os.stat(app_file)
    os.chmod(app_file, st.st_mode | stat.S_IEXEC)

    # prepend $PATH and $PYTHONPATH to rcfile
    if rcfile is None:
        rcfile = _lookup_rcfile(interactive=False)

    with open(rcfile, mode="at") as fileh:
        fileh.write(
            "\n".join(
                [
                    f"# Created by {THIS_FILE}",
                    f"export PATH={install_dir}:$PATH",
                    f"export PYTHONPATH={REPO_DIR}:$PYTHONPATH\n",
                ]
            )
        )

    print(
        "Installation complete. "
        "To start using pyw, please open a new terminal, or run\n"
        f"source {rcfile}"
    )
