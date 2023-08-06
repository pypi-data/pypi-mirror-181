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
['Jinja2>=3.1.2,<4.0.0', 'click>=8.1.3,<9.0.0', 'pygame>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['cubone = cubone.cli.core:main']}

setup_kwargs = {
    'name': 'cubone',
    'version': '0.1.2',
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
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
