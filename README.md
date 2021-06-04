# wxc

[![PyPI](https://img.shields.io/pypi/v/wxc)](https://pypi.org/project/wxc/)
[![codecov](https://codecov.io/gh/neutrinoceros/wxc/branch/master/graph/badge.svg)](https://codecov.io/gh/neutrinoceros/wxc)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/neutrinoceros/wxc/main.svg)](https://results.pre-commit.ci/latest/github/neutrinoceros/wxc/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`wxc` (pronounced "which") allows you to inspect source code in your Python
environment from the command line. It is based on the `inspect` module from the
standard library.


In essence,
```shell
$ wxc pandas
```
is equivalent to
```shell
$ python -c "import pandas; print(pandas.__file__)"
```

`wxc` can also be used to navigate source code, by locating classes and
functions by `file:line number`
```shell
$ wxc pandas.DataFrame
/path/to/your/env/site-packages/pandas/core/frame.py:319
```
which is extremely convenient when combined with augmented terminal applications
such as [`iterm2`](https://iterm2.com).

## Installation

```shell
$ pip install wxc
```
Note that `wxc` should never be installed in isolation (for instance via
[pipx](https://pipxproject.github.io/pipx/)) since it would completely defeat
the purpose.

## Usage

Examples

```shell
$ wxc numpy
/path/to/your/env/site-packages/numpy

$ wxc pandas --version
1.0.3

$ wxc stdlib_list --full
source = /path/to/your/env/site-packages/stdlib_list/__init__.py:0
version = v0.8.0
in_stdlib = False
name = stdlib_list
```

## Known limitations

`wxc` is not able to retrieve the source of compiled code binded into Python. It
should however correctly point to the compiled file that an object is imported
from.

## Notes

- `wxc` is tested on macOS, Linux, from Python 3.6 to 3.10
- for Python versions older than 3.10, `wxc` relies on
  [stdlib_list](https://github.com/jackmaney/python-stdlib-list) to determine
  which packages are part of the standard library.
- this project was formerly named "whych" and renamed to avoid confusion with the
  pypi-available package of the same name.
