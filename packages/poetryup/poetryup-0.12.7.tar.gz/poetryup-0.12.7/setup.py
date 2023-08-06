# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poetryup', 'poetryup.core', 'poetryup.models']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=21.3,<22.0', 'tomlkit>=0.11.0,<0.12.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['poetryup = poetryup.main:app']}

setup_kwargs = {
    'name': 'poetryup',
    'version': '0.12.7',
    'description': 'Update dependencies and bump their version in the pyproject.toml file',
    'long_description': "# PoetryUp\n\n![build](https://github.com/MousaZeidBaker/poetryup/workflows/Publish/badge.svg)\n![test](https://github.com/MousaZeidBaker/poetryup/workflows/Test/badge.svg)\n[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)\n![python_version](https://img.shields.io/badge/python-%3E=3.6-blue)\n[![pypi_v](https://img.shields.io/pypi/v/poetryup)](https://pypi.org/project/poetryup)\n[![pypi_dm](https://img.shields.io/pypi/dm/poetryup)](https://pypi.org/project/poetryup)\n\n\n> __Warning__\n>\n> This package has been deprecated and is no longer maintained, `poetryup` has moved to [poetry-plugin-up](https://github.com/MousaZeidBaker/poetry-plugin-up)\n\nPoetryUp updates dependencies and bumps their version in both `poetry.lock` as\nwell as in `pyproject.toml` file. Dependencies version constraints are\nrespected, unless the `--latest` flag is passed, in which case dependencies will\nbe updated to their latest available version. PoetryUp runs\n[poetry](https://github.com/python-poetry/poetry) commands, thus it's required\nto be installed. The difference between running `poetry update` and `poetryup`,\nis that the latter also modifies the `pyproject.toml` file.\n\n![poetryup_demo](https://raw.githubusercontent.com/MousaZeidBaker/poetryup/master/media/poetryup_demo.gif)\n\n## Usage\n\nShow help message and exit\n```shell\npoetryup --help\n```\n\nUpdate all dependencies with respect to their version constraints specified in the\n`pyproject.toml` file\n```shell\npoetryup\n```\n\nUpdate all dependencies to their latest available version\n```shell\npoetryup --latest\n```\n\nUpdate all dependencies to their latest available version except for packages\nwith an exact version\n```shell\npoetryup --latest --skip-exact\n```\n\nUpdate dependencies in the `default` and `dev` group to their latest available version\n```shell\npoetryup --latest --group default --group dev\n```\n\nUpdate the `foo` and `bar` dependencies to their latest available version\n```shell\npoetryup --latest --name foo --name bar\n```\n\nUpdate all dependencies to their latest available version except the `foo` and `bar` dependencies\n```shell\npoetryup --latest --exclude-name foo --exclude-name bar\n```\n\n## Contributing\n\nContributions are welcome! See the [Contributing Guide](https://github.com/MousaZeidBaker/poetryup/blob/master/CONTRIBUTING.md).\n\n## Issues\n\nIf you encounter any problems, please file an\n[issue](https://github.com/MousaZeidBaker/poetryup/issues) along with a\ndetailed description.\n",
    'author': 'Mousa Zeid Baker',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MousaZeidBaker/poetryup',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
