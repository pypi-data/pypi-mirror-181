# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfdupes']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.5,<0.5.0']

entry_points = \
{'console_scripts': ['pyfdupes = pyfdupes.cli:run']}

setup_kwargs = {
    'name': 'pyfdupes',
    'version': '0.1.0',
    'description': 'Find and delete duplicate files using fdupes',
    'long_description': '![Github](https://img.shields.io/github/tag/essembeh/pyfdupes.svg)\n![PyPi](https://img.shields.io/pypi/v/pyfdupes.svg)\n![Python](https://img.shields.io/pypi/pyversions/pyfdupes.svg)\n![CI](https://github.com/essembeh/pyfdupes/actions/workflows/poetry.yml/badge.svg)\n\n# pyfdupes\n\nCommand line tool to find and delete duplicate files in folders using `fdupes`.\n\n# Install\n\nInstall dependencies\n\n```sh\n$ sudo apt update\n$ sudo apt install fdupes\n```\n\nInstall the latest release of _pyfdupes_ from [PyPI](https://pypi.org/project/pyfdupes/)\n\n```sh\n$ pip3 install pyfdupes\n$ pyfdupes --help\n```\n\nOr install _pyfdupes_ from the sources\n\n```sh\n$ pip3 install poetry\n$ pip3 install git+https://github.com/essembeh/pyfdupes\n$ pyfdupes --help\n```\n',
    'author': 'Sébastien MB',
    'author_email': 'seb@essembeh.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/essembeh/pyfdupes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
