<img src="logo.jpg"
     alt="whych logo"
     height="80"
     style="float: left; margin-right: 10px;" />
     
[![codecov](https://codecov.io/gh/neutrinoceros/whych/branch/master/graph/badge.svg)](https://codecov.io/gh/neutrinoceros/whych)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

whych is a command line tool to interogate your Python installation.
In essence,

```bash
>> whych pandas
```
is equivalent to
```bash
>> python -c "import pandas; print(pandas.__path__)"
```

whych provides additional functionalities to:
- retrieve the package's version with `-v/--version`
- generate a small report with `-i/--info`.

## Installation

Because whych is mostly useful if you use a python enviroment manager (conda ...), it is recommended to install this in your "base" environment, so that it remains available as you switch environments.

From the top level of the repo, run
```bash
pip install -e .
```


## Usage

### CLI

Examples
```bash
>> whych numpy
/Users/yourname/miniconda3/envs/production/lib/python3.8/site-packages/numpy

>> whych pandas --version
1.0.3

>> whych vtk --info
module name: vtk
path: /Users/yourname/miniconda3/envs/production/lib/python3.8/site-packages/vtkmodules
version: unknown
last updated: 2020-05-22 11:31:18
stdlib: False
```
Note that `whych` will replace any unknow value with `"unknown"`.
In this example, the `vtk` package does not have a `__version__` attribute.

### From a python session

Equivalent to the CLI examples above
```python
>> from whych import whych

>> print(whych("numpy"))
>> print(whych("pandas", query="version"))
>> print(whych("vtk", query="info"))
```

Additionally, the module data obtained with `query="info"` can be retrived as a dictionnary with
```python
>> from whych import WhychFinder
>> wf = WhychFinder()
>> wf.get_data("vtk")
{'last updated': '2020-05-22 11:31:18',
 'module name': 'vtk',
 'path': '/Users/yourname/miniconda3/envs/production/lib/python3.8/site-packages/vtkmodules',
 'stdlib': False,
 'version': 'unknown'}
```

## Dependencies
- whych is tested on macOS, Linux and Windows against Python 3.8, and should be backwards compatible down to Python 3.6
- whych relies on [stdlib_list](https://github.com/jackmaney/python-stdlib-list) to determine which packages are part of the standard library.
