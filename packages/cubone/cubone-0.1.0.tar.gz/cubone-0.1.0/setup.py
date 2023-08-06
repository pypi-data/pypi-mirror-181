# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cubone',
 'cubone.cli',
 'cubone.modules',
 'cubone.modules.network',
 'cubone.tests']

package_data = \
{'': ['*']}

install_requires = \
['pygame>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'cubone',
    'version': '0.1.0',
    'description': 'A pygame scaffold package',
    'long_description': None,
    'author': 'Francisco',
    'author_email': 'vieirafrancisco.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
