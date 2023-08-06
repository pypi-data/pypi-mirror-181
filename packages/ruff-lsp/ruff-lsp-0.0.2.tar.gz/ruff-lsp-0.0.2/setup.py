# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ruff_lsp']

package_data = \
{'': ['*']}

install_requires = \
['pygls>1.0.0a3', 'ruff', 'typing_extensions']

entry_points = \
{'console_scripts': ['ruff-lsp = ruff_lsp.__main__:main']}

setup_kwargs = {
    'name': 'ruff-lsp',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'Charlie Marsh',
    'author_email': 'charlie.r.marsh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
