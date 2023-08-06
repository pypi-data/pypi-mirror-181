# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['makeflatt']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'makeflatt',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Jonathan Schweder',
    'author_email': 'jonathanschweder@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
