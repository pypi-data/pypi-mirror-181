# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soccer_sdk_utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'soccer-sdk-utils',
    'version': '0.1.3',
    'description': 'A utility library for Soccer SDK packages.',
    'long_description': 'None',
    'author': 'Omar Crosby',
    'author_email': 'omar.crosby@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
