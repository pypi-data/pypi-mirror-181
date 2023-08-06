# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['interprog']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'interprog',
    'version': '0.2.0',
    'description': 'Inter-process progress reports made easy',
    'long_description': "# Interprog\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n [![codecov](https://codecov.io/gh/ThatXliner/interprog/branch/main/graph/badge.svg)](https://codecov.io/gh/ThatXliner/interprog) [![Documentation Status](https://readthedocs.org/projects/interprog/badge/?version=latest)](https://interprog.readthedocs.io/en/latest/?badge=latest) [![CI](https://github.com/ThatXliner/interprog/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ThatXliner/interprog/actions/workflows/ci.yml) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/interprog)](https://pypi.org/project/interprog) [![PyPI](https://img.shields.io/pypi/v/interprog)](https://pypi.org/project/interprog) [![PyPI - License](https://img.shields.io/pypi/l/interprog)](#license)\n\n> Inter-process progress reports made easy\n\n\n## Installation\n\nYou can get this project via `pip`\n\n```bash\n$ pip install interprog\n```\n\nOr, if you're using [Poetry](https://python-poetry.org)\n\n```bash\n$ poetry add interprog\n```\n\n\n## License\n\nCopyright © 2022, Bryan Hu\n\nThis project is licensed under the [MIT](https://github.com/ThatXliner/interprog/blob/main/LICENSE.txt).\n",
    'author': 'Bryan Hu',
    'author_email': 'bryan.hu.2020@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ThatXliner/interprog',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
