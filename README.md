<img src="logo.jpg"
     alt="whych logo"
     height="80"
     style="float: left; margin-right: 10px;" />
     
[![codecov](https://codecov.io/gh/neutrinoceros/whych/branch/master/graph/badge.svg)](https://codecov.io/gh/neutrinoceros/whych)

whych is a command line tool to interogate your Python installation.
In essence,

```bash
>> whych pandas
# and
>> python -c "import pandas; print(pandas.__path__)"
```
are equivalent, though whych can also retrieve the package's version with `-v/--version`, or both path and version with `-i/--info`.

## Installation

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
>> from pprint import pprint
>> from whych import WhychFinder
>> data = WhychFinder("vtk").get_data()
>> pprint(data)
{'module name': 'vtk',
'path': '/Users/yourname/miniconda3/envs/production/lib/python3.8/site-packages/vtkmodules',
'version': 'unknown'}
```
