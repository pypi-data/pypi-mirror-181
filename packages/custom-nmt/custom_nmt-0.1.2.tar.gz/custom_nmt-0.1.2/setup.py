# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['custom_nmt']

package_data = \
{'': ['*'], 'custom_nmt': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['tensorflow-macos>=2.10.0,<3.0.0', 'tensorflow-metal>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'custom-nmt',
    'version': '0.1.2',
    'description': '',
    'long_description': '',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
