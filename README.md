# whych

`whych` is a CL-tool to retrieve a Python's package location on disk.
In essence, `whych pandas` is the same as `python -c "import pandas; print(pandas.__version__)"`, though `whych` can also retrieve the package's version with `-v`, or both path and version with `-i`.

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
/Users/yourname/miniconda3/envs/production/lib/python3.8/site-packages/numpy/__init__.py

>> whych pandas --version
1.0.3

>> whych vtk --info
module name: vtk
path: /Users/yourname/miniconda3/envs/production/lib/python3.8/site-packages/vtkmodules/all.py
version: unknown
```
Note that `whych` will replace any unknow value with `"unknown"`.
In this example, the `vtk` package does not have a `__version__` attribute.

### From a python session

Equivalent to the CLI examples above
```python
from whych import whych

print(whych("numpy"))
print(whych("pandas", query="version"))
print(whych("vtk", query="info"))
```

Additionally, the module data obtained with `query="info"` can be retrived as a dictionnary with
```python
from whych import WhychFinder
data = WhychFinder("vtk").get_data()
```

so it can be stored as json
```python
import json
with open("package-data.json", mode="wt") as fileobj:
  json.dump(fileobj, data)
```
