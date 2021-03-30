<img src="logo.jpg"
     alt="pyw logo"
     height="100"
     style="float: left; margin-right: 10px;" />

<!-- ![PyPI](https://img.shields.io/pypi/v/pyw) -->
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/neutrinoceros/whych)
[![codecov](https://codecov.io/gh/neutrinoceros/pyw/branch/master/graph/badge.svg)](https://codecov.io/gh/neutrinoceros/pyw)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/neutrinoceros/pyw/main.svg)](https://results.pre-commit.ci/latest/github/neutrinoceros/pyw/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

pyw is a command line tool to explore your python environment, wrapping functionalities from the very useful but fragile builtin module `inspect`.

In essence,
```shell
$ pyw pandas
```
is equivalent to
```shell
$ python -c "import pandas; print(pandas.__file__)"
```

pyw can also be used to navigate source code, by locating classes and functions by `file:line

```shell
$ pyw pandas.DataFrame
/Users/yourname/miniconda3/envs/production/lib/python3.8/site-packages/pandas/core/frame.py:319
```

## Installation

Here's the recommended installation method
```shell
$ pip install git+https://github.com/neutrinoceros/pyw@main
```

> Note that `pyw` should never be installed in isolation (for instance via
[pipx](https://pipxproject.github.io/pipx/)) because it completely defeats the
purpose.
## Usage

Examples

```shell
$ pyw numpy
/Users/yourname/miniconda3/envs/production/lib/python3.8/site-packages/numpy

$ pyw pandas --version
1.0.3

$ pyw stdlib_list --full
source = <>pyw_dev/lib/python3.9/site-packages/stdlib_list/__init__.py:0
version = v0.8.0
in_stdlib = False
name = stdlib_list
```

## Notes
- the Python api is tested on macOS, Linux, for Python 3.6 and 3.9
- pyw relies on [stdlib_list](https://github.com/jackmaney/python-stdlib-list)
  to determine which packages are part of the standard library.
- this project was formerly named "whych" and renamed to avoid confusion with the
  pypi-available package of the same name.
