# wxc

[![PyPI](https://img.shields.io/pypi/v/wxc)](https://pypi.org/project/wxc/)
[![codecov](https://codecov.io/gh/neutrinoceros/wxc/branch/master/graph/badge.svg)](https://codecov.io/gh/neutrinoceros/wxc)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/neutrinoceros/wxc/main.svg)](https://results.pre-commit.ci/latest/github/neutrinoceros/wxc/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`wxc` (pronounced "which") is a command line tool to query the current Python environment, wrapping functionalities from the very useful but fragile builtin module `inspect`.

In essence,
```shell
$ wxc pandas
```
is equivalent to
```shell
$ python -c "import pandas; print(pandas.__file__)"
```

`wxc` can also be used to navigate source code, by locating classes and functions by `file:line number`
```shell
$ wxc pandas.DataFrame
/Users/yourname/miniconda3/envs/production/lib/python3.8/site-packages/pandas/core/frame.py:319
```
which is extremely conveninent when combined with augmented terminal applications such as [`iterm2`](https://iterm2.com)

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
/Users/yourname/miniconda3/envs/production/lib/python3.8/site-packages/numpy

$ wxc pandas --version
1.0.3

$ wxc stdlib_list --full
source = /Users/yourname/miniconda3/envs/production/lib/python3.9/site-packages/stdlib_list/__init__.py:0
version = v0.8.0
in_stdlib = False
name = stdlib_list
```

## Notes
- the Python api is tested on macOS, Linux, for Python 3.6 and 3.9
- `wxc` relies on [stdlib_list](https://github.com/jackmaney/python-stdlib-list)
  to determine which packages are part of the standard library.
- this project was formerly named "whych" and renamed to avoid confusion with the
  pypi-available package of the same name.
