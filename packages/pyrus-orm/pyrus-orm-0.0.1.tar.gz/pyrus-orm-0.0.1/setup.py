# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrus_orm']

package_data = \
{'': ['*']}

install_requires = \
['pyrus-api>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'pyrus-orm',
    'version': '0.0.1',
    'description': "Radically simple ORM for Pyrus's tasks",
    'long_description': None,
    'author': 'Alexey Sveshnikov',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
