# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyxrayc', 'pyxrayc.cli']

package_data = \
{'': ['*']}

install_requires = \
['python-decouple>=3.6,<4.0',
 'typer[all]>=0.7.0,<0.8.0',
 'typing-extensions>=4.4.0,<5.0.0',
 'ujson>=5.6.0,<6.0.0']

entry_points = \
{'console_scripts': ['pyxrayc = pyxrayc.cli.main:app']}

setup_kwargs = {
    'name': 'pyxrayc',
    'version': '0.1.3',
    'description': 'CLI utility for managing Xray VPN server user accounts with ease, written in Python.',
    'long_description': '<div align="center">\n<h1><a href="https://github.com/PlumaCompanyLtd/PyXrayC"><b>PyXrayC</b></a></h1>\n<a href="https://github.com/PlumaCompanyLtd/PyXrayC/actions?query=workflow%3APublish" target="_blank">\n    <img src="https://github.com/PlumaCompanyLtd/PyXrayC/workflows/Publish/badge.svg" alt="Publish">\n</a>\n<a href="https://www.python.org">\n    <img src="https://img.shields.io/pypi/pyversions/pyxrayc.svg" alt="Python Versions">\n</a>\n<a href="https://github.com/PlumaCompanyLtd/PyXrayC">\n    <img src="https://img.shields.io/pypi/v/pyxrayc.svg" alt="PyPI Version">\n</a>\n<a href="https://github.com/psf/black">\n    <img src="https://img.shields.io/static/v1?label=code%20style&message=black&color=black&style=flat" alt="Code Style: black">\n</a>\n<a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat" alt="pre-commit">\n</a>\n</div>\n\n## Introduction\n\n_PyXrayC_ is a CLI tool built with Python and [Typer] library that helps you to manage your [Xray] VPN server\'s user\naccounts with ease.\n\n## Features\n\n- Installable via `pip`\n- Fully type hinted and extensible code base.\n- User friendly and easy to use interface.\n- Optional shell autocompletion.\n- Add, view or delete users to/from your config file.\n\n## Requirements\n\n- A Linux distribution with [Xray] VPN server installed on it.\n- Python 3.8 or higher.\n\n## Installation\n\nYou can install _PyXrayC_ from [PyPI](https://pypi.org/project/pyxrayc/) using pip:\n\n```bash\n$ pip3 install pyxrayc\n```\n\n## Usage\n\nYou can see _PyXrayC_\'s help message by running:\n\n```bash\n$ pyxrayc --help\n```\n\n## Configuration\n\n_PyXrayC_ uses below environment variables as its configuration:\n\n- `XRAY_CONFIG_PATH`: Path to the config file. Default: `/usr/local/etc/xray/config.json`\n- `XRAY_BACKUP_PATH`: Path to the backup file. Default: `/usr/local/etc/xray/backup.json`\n\n## License\n\nThis project is licensed under the terms of the [GPL-3.0] licence.\n\n<p align="center">&mdash; ⚡ &mdash;</p>\n\n<!-- Links -->\n\n[GPL-3.0]: https://www.gnu.org/licenses/gpl-3.0.en.html "GNU General Public License v3.0"\n[typer]: https://github.com/tiangolo/typer "Typer, build great CLIs. Easy to code. Based on Python type hints."\n[xray]: https://github.com/XTLS "Project X"\n',
    'author': 'Seyed',
    'author_email': 'pyseyed@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/PlumaCompanyLtd/PyXrayC',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
