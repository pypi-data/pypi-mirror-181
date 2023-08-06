# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['msproject']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'msproject',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'mrebu',
    'author_email': 'm.rebuglio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
