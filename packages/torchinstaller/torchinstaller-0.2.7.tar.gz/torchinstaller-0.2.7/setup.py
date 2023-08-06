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
    'version': '0.2.7',
    'description': '',
    'long_description': '# PyTorch Install Helper\n\nSuper basic helper to install pytorch stuff without having to check cuda versions and go to websites for the installer URLs.\n\n> _Only Linux and macOS Supported_\n\nDetects what cuda version is available and runs the pip command to install latest pytorch and compatible cuda version\n\n## Installation \n\n```bash\npip install torchinstaller\n```\n\n\n## Usage\n\n```bash\n$ torchinstall -h\nusage: torchinstall [-h] [--poetry] [--dryrun] [--pyg] [--lightning]\n\noptional arguments:\n  -h, --help       show this help message and exit\n  --poetry, -p     Uses poetry for install. Creates a torch source and adds torch to pyproject.toml\n  --dryrun, -d     just prints the commands that would be run\n  --pyg, -pyg      Flag to also install pytorch-geometric\n  --lightning, -l  Flag to also install pytorch-lightning\n```\n\n> Note: poetry support is a work in-progress and is unstable\n\n\n',
    'author': 'Daniel Capecci',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
