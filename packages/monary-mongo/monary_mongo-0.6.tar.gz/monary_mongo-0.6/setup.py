# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monary_mongo']

package_data = \
{'': ['*']}

install_requires = \
['numpy']

setup_kwargs = {
    'name': 'monary-mongo',
    'version': '0.6',
    'description': 'Monary performs high-performance column queries on MongoDB',
    'long_description': 'None',
    'author': 'Andrew Gigena',
    'author_email': 'mail@andrewgigena.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/andrewgigena/monary_mongo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
