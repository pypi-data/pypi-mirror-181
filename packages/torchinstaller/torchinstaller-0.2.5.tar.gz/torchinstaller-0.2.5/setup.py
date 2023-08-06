# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchinstaller']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['torchinstall = torchinstaller.main:main']}

setup_kwargs = {
    'name': 'torchinstaller',
    'version': '0.2.5',
    'description': '',
    'long_description': '# PyTorch Install Helper\n\n> _Only Linux and macOS Supported_\n\nDetects what cuda version is available and runs the pip command to install latest pytorch and compatible cuda version\n',
    'author': 'Daniel Capecci',
    'author_email': 'capeccid@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
