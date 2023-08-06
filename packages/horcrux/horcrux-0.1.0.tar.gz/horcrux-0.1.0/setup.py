# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shamir', 'shamir.math', 'shamir.utils']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=38.0.4,<39.0.0']

setup_kwargs = {
    'name': 'horcrux',
    'version': '0.1.0',
    'description': "Horcrux - A Python implementation of Shamir's Secret Sharing.",
    'long_description': 'None',
    'author': 'Reid Hochstedler',
    'author_email': 'reidhoch@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/reidhoch/horcrux',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
