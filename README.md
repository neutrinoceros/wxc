# wxc

[![PyPI](https://img.shields.io/pypi/v/wxc.svg?logo=pypi&logoColor=white&label=PyPI)](https://pypi.org/project/wxc/)
[![](https://img.shields.io/badge/contributions-welcome-brightgreen)](https://github.com/neutrinoceros/wxc/pulls)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/neutrinoceros/wxc/main.svg)](https://results.pre-commit.ci/latest/github/neutrinoceros/wxc/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)


`wxc` (pronounced "which") allows you to inspect source code in your Python
environment from the command line. It is based on the `inspect` module from the
standard library.


## Installation

```shell
$ python -m pip install wxc
```

## Usage

Get the version number of a package in your current environment
<p align="center">
    <img src="https://raw.githubusercontent.com/neutrinoceros/wxc/main/gallery/example_version.png" width="800"></a>
</p>

Locate the file from which a Python package is imported
<p align="center">
    <img src="https://raw.githubusercontent.com/neutrinoceros/wxc/main/gallery/example_loc.png" width="800"></a>
</p>

Locate a specific method's source code
<p align="center">
    <img src="https://raw.githubusercontent.com/neutrinoceros/wxc/main/gallery/example_method.png" width="800"></a>
</p>

View the source code of function directly from the terminal stdout
<p align="center">
    <img src="https://raw.githubusercontent.com/neutrinoceros/wxc/main/gallery/example_source.png" width="800"></a>
</p>


`wxc` tries to be helpful when you mistype
<p align="center">
    <img src="https://raw.githubusercontent.com/neutrinoceros/wxc/main/gallery/example_resilience.png" width="800"></a>
</p>

For more, run
```shell
$ wxc --help
```

## Known limitations

`wxc` is not currently able to retrieve the source of compiled code binded into
Python. It should however correctly point to the compiled file that an object is
imported from.

`wxc` should never be installed in isolation (for instance via
[pipx](https://pipxproject.github.io/pipx/)) since it would completely defeat
its purpose.

## Notes

- `wxc` is fully tested on macOS, Linux, and partially on Windows
- this project was formerly named "whych" and renamed to avoid confusion with the
  pypi-available package of the same name.
