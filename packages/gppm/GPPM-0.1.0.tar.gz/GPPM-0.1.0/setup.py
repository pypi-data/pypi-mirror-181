# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gppm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gppm',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Owen Plimer',
    'author_email': 'o.plimer@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Owen7000/General-Purpose-Python-Module',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
