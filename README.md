# wxc

[![PyPI](https://img.shields.io/pypi/v/wxc.svg?logo=pypi&logoColor=white&label=PyPI)](https://pypi.org/project/wxc/)
[![PyPI](https://img.shields.io/pypi/pyversions/wxc?logo=python&logoColor=white&label=Python)](https://pypi.org/project/wxc/)
[![](https://img.shields.io/badge/contributions-welcome-brightgreen)](https://github.com/neutrinoceros/wxc/pulls)

[![codecov](https://codecov.io/gh/neutrinoceros/wxc/branch/master/graph/badge.svg)](https://codecov.io/gh/neutrinoceros/wxc)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/neutrinoceros/wxc/main.svg)](https://results.pre-commit.ci/latest/github/neutrinoceros/wxc/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`wxc` (pronounced "which") allows you to inspect source code in your Python
environment from the command line. It is based on the `inspect` module from the
standard library.


## Installation

```shell
$ python3 -m pip install wxc
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

`wxc`'s resilience against mistakes
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

- `wxc` is tested on macOS, Linux, and partially on Windows, from Python 3.6 to 3.10 (beta)
- from Python 3.10, `wxc` currently has no dependencies outside of the standard
  library.
- this project was formerly named "whych" and renamed to avoid confusion with the
  pypi-available package of the same name.
