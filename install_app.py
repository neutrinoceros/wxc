from pathlib import Path

this_file = Path(__file__).resolve()
repo_dir = this_file.parent
app_dir = repo_dir / ".app"

try:
    app_dir.mkdir()
except FileExistsError:
    print(
        f"{app_dir} already exists. "
        "Please remove this directory before installing again. "
        "You might also need to cleanup your shell rc file."
    )
    exit(1)

app_file = app_dir / "whych"

app_file.symlink_to(repo_dir.joinpath("whych", "__main__.py"))

# prepend $PATH and $PYTHONPATH
lookup_table = [".zshrc", ".bashrc", ".bash_profile"]
found = [file for file in lookup_table if (Path.home() / file).is_file()]
if not found:
    raise FileNotFoundError("Could not determine your shell configuration file")

if len(found) > 1:
    filename = ""
    while filename not in found:
        filename = input(
            "Please select your shell configuration file "
            f"({', '.join(found)}))    "
        )
    conf_file = Path.home() / filename
else:
    conf_file = Path.home() / found[0]

with open(conf_file, mode="at") as fileh:
    fileh.write(
        "\n".join(
            [
                f"# Created by {this_file}",
                f"export PATH={app_dir}:$PATH",
                f"export PYTHONPATH={repo_dir}:$PATH\n",
            ]
        )
    )

print(
    "Installation complete. "
    "To start using whych, please open a new terminal, or run\n"
    f"source {conf_file}"
)
