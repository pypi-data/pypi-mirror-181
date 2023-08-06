# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uai_pre_import_transform_interface']

package_data = \
{'': ['*']}

install_requires = \
['uai-uri-interface>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'uai-pre-import-transform-interface',
    'version': '0.1.0',
    'description': '',
    'long_description': "This package provides an Interface that can be implemented to then be turned into a job.\nThe used URI interface (pre_import_transform_interface/path_interface.py) is basically a [pathlib.Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path) with some missing functionality.\n\nEvery implementation should provide a python package named by you. Let's use `package_name` as an example. From this package the following import has to work:\n```python\nfrom package_name import PreImportTransformer\n```\nThis should give your implementation of the interface.",
    'author': 'understand.ai',
    'author_email': 'postmaster@understand.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
