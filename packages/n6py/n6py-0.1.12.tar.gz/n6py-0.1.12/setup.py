# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['n6py', 'n6py.encode', 'n6py.stats']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.5,<2.0.0', 'pandas>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'n6py',
    'version': '0.1.12',
    'description': 'N6 AI Python Tools',
    'long_description': '# N6 Py\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/n6py?color=%23141414&style=for-the-badge)](https://pypi.org/project/n6py)\n[![Package Status](https://img.shields.io/pypi/status/n6py?color=%23141414&style=for-the-badge)](https://pypi.org/project/n6py)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-141414.svg?style=for-the-badge)](https://github.com/psf/black)\n\n## About\n\nN6 AI Python Tools.\n\nTooling for common problems in Scientific Computing, Machine Learning and Deep Learning.\n\n## Installing\n\n**pip**\n\n```sh\npip install n6py\n```\n\n**Poetry**\n\n```sh\npoerty add n6py\n```\n\n## Using\n\nTo use the `n6py` package import it into your project.\n\n```py\nimport n6py as n6\n```\n\n## Development\n\n### Prerequisites\n\n- [Python v3+](https://www.python.org/downloads/)\n- [Poetry](https://python-poetry.org/)\n\n### Installing\n\n```sh\npoetry install\npoetry run pre-commit install\n```\n',
    'author': 'Sergej Samsonenko',
    'author_email': 'contact@sergej.codes',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/n6ai/n6py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
