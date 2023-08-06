This package provides an Interface that can be implemented to then be turned into a job.
The used URI interface (pre_import_transform_interface/path_interface.py) is basically a [pathlib.Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path) with some missing functionality.

Every implementation should provide a python package named by you. Let's use `package_name` as an example. From this package the following import has to work:
```python
from package_name import PreImportTransformer
```
This should give your implementation of the interface.