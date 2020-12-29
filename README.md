<img src="logo.jpg"
     alt="whych logo"
     height="80"
     style="float: left; margin-right: 10px;" />

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/neutrinoceros/whych)
[![codecov](https://codecov.io/gh/neutrinoceros/whych/branch/master/graph/badge.svg)](https://codecov.io/gh/neutrinoceros/whych)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/neutrinoceros/whych/master.svg)](https://results.pre-commit.ci/latest/github/neutrinoceros/whych/master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

whych is a command line tool to interogate your Python installation.
In essence,

```shell
$ whych pandas
```
is equivalent to
```shell
$ python -c "import pandas; print(pandas.__file__)"
```

whych can also be used to navigate source code, by locating classes and functions by file+line

```shell
$ whych pandas.DataFrame
/Users/yourname/miniconda3/envs/production/lib/python3.8/site-packages/pandas/core/frame.py:319
```

## Installation

### Command line app

``whych``'s command line application shines most if you use isolated Python
environments. In order to make it available from anywhere on your system and
against the current environment run
```shell
$ python install_app.py
```
:warning: Currently only Linux and MacOS are supported. On Windows, it is still
possible to install `whych` on an specific environment by installing the Python
package (see next section).

### Python api

From the top level of the repo, run
```shell
$ pip install -e .
```

This will make `whych`'s internal functionalities available from a Python
session in the current environment.


## Usage

### On the command line

Examples

```shell
$ whych numpy
/Users/yourname/miniconda3/envs/production/lib/python3.8/site-packages/numpy

$ whych pandas --version
1.0.3

$ whych vtk --info
is_available: True
is_module: True
is_stdlib: False
last_updated: 2020-09-28 19:52:03
line: 0
member: vtk
module_name: vtkmodules.all
package_name: vtk
path: /Users/yourname/miniconda3/envs/project/lib/python3.8/site-packages/vtkmodules/all.py
version: 9.0.1
```

### From a Python session

Equivalent to the CLI examples above
```python
import whych
print(
     whych.query("numpy", field="path"),
     whych.query("pandas", field="version"),
     whych.query("vtk", field="info")
)
```

Alternatively, use `whych.get_data()`, which returns dictionaries:
```python
import whych
print(
     whych.get_data("numpy")["path"],
     whych.get_data("numpy")["version"],
     whych.get_data("vtk")
)
```

## Notes
- the Python api is tested on macOS, Linux and Windows, for Python 3.8 and 3.9
  It should be possible to run it against Python 3.6 with the additional
  requirement that `importlib_metadata` is installed in the runtime environment.
- whych relies on [stdlib_list](https://github.com/jackmaney/python-stdlib-list)
  to determine which packages are part of the standard library.
- whych tries to determine the source file from which the object is imported. In
  some cases (e.g. for the standard library on Windows), it will fall back to a
  directory.
