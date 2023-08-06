# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['makeflatt']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'makeflatt',
    'version': '1.0.2',
    'description': 'Simple library to make your dictionary flatten',
    'long_description': '# MakeFlatt\n> Simple library to make your dictionary flatten in Python\n\n[![PyPI version](https://badge.fury.io/py/makeflatt.svg)](https://badge.fury.io/py/makeflatt)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/makeflatt)\n[![Unit Tests](https://github.com/jaswdr/makeflatt/actions/workflows/unit-tests.yml/badge.svg?branch=master)](https://github.com/jaswdr/makeflatt/actions/workflows/unit-tests.yml)\n![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)\n![PyPI - License](https://img.shields.io/pypi/l/makeflatt)\n\n\n### Installation\n\n```bash\npip install makeflatt\n```\n\n### Usage\n\nQuick start:\n\n```python\n>>> from makeflatt import FlattMaker\n>>> mf = FlattMaker()\n>>> mf.apply({"a": {"b": {"c": "test"}}})\n{\'a.b.c\': \'test\'}\n```\n\nMake nested structured flatten without expanding lists:\n\n```python\n>>> mf.apply({"a": {"b": ["b1", "b2", "b3"]}})\n{\'a.b\': [\'b1\', \'b2\', \'b3\']}\n```\n\nOr use `deep_apply` to also expand lists:\n\n```python\n>>> mf.deep_apply({"a": {"b": ["b1", "b2", "b3"]}})\n{\'a.b.0\': \'b1\', \'a.b.1\': \'b2\', \'a.b.2\': \'b3\'}\n```\n\nYou can also change the separator and define your own:\n\n```python\n>>> mf = FlattMaker(sep=":")\n>>> mf.apply({"a": {"b": ["b1", "b2", "b3"]}})\n{\'a:b\': [\'b1\', \'b2\', \'b3\']}\n```\n\n### License\n\nMakeflatt is released under the MIT Licence. See the bundled LICENSE file for details.\n\n### Development\n\nCheck the [CONTRIBUTING](CONTRIBUTING.md) file.\n\n### Versioning\n\nThis package attempts to use semantic versioning. API changes are indicated by the major version, non-breaking improvements by the minor, and bug fixes in the revision.\n\nIt is recommended that you pin your targets to greater or equal to the current version and less than the next major version.\n\n### Maintainer\n\nCreated and maitained by Jonathan Schweder (@jaswdr)\n',
    'author': 'Jonathan Schweder',
    'author_email': 'jonathanschweder@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jaswdr/makeflatt',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
