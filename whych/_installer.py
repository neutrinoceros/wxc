from pathlib import Path


def _lookup_rcfile(interactive: bool):
    lookup_table = [".zshrc", ".bashrc", ".bash_profile"]
    found = [file for file in lookup_table if (Path.home() / file).is_file()]
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
    this_file = Path(__file__).resolve()
    repo_dir = this_file.parents[1]
    if install_dir is None:
        install_dir = repo_dir / ".app"

    install_dir = Path(install_dir)

    try:
        install_dir.mkdir()
    except FileExistsError:
        print(
            f"{install_dir} already exists. "
            "Please remove this directory before installing again. "
            "You might also need to cleanup your shell rc file."
        )
        exit(1)

    app_file = install_dir / "whych"

    app_file.symlink_to(repo_dir.joinpath("whych", "__main__.py"))

    # prepend $PATH and $PYTHONPATH
    if rcfile is None:
        rcfile = _lookup_rcfile(interactive=False)

    with open(rcfile, mode="at") as fileh:
        fileh.write(
            "\n".join(
                [
                    f"# Created by {this_file}",
                    f"export PATH={install_dir}:$PATH",
                    f"export PYTHONPATH={repo_dir}:$PATH\n",
                ]
            )
        )

    print(
        "Installation complete. "
        "To start using whych, please open a new terminal, or run\n"
        f"source {rcfile}"
    )
