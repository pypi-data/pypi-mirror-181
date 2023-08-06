<div align="center">
<h1><a href="https://github.com/PlumaCompanyLtd/PyXrayC"><b>PyXrayC</b></a></h1>
<a href="https://github.com/PlumaCompanyLtd/PyXrayC/actions?query=workflow%3APublish" target="_blank">
    <img src="https://github.com/PlumaCompanyLtd/PyXrayC/workflows/Publish/badge.svg" alt="Publish">
</a>
<a href="https://www.python.org">
    <img src="https://img.shields.io/pypi/pyversions/pyxrayc.svg" alt="Python Versions">
</a>
<a href="https://github.com/PlumaCompanyLtd/PyXrayC">
    <img src="https://img.shields.io/pypi/v/pyxrayc.svg" alt="PyPI Version">
</a>
<a href="https://github.com/psf/black">
    <img src="https://img.shields.io/static/v1?label=code%20style&message=black&color=black&style=flat" alt="Code Style: black">
</a>
<a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat" alt="pre-commit">
</a>
</div>

## Introduction

_PyXrayC_ is a CLI tool built with Python and [Typer] library that helps you to manage your [Xray] VPN server's user
accounts with ease.

## Features

- Installable via `pip`
- Fully type hinted and extensible code base.
- User friendly and easy to use interface.
- Optional shell autocompletion.
- Add, view or delete users to/from your config file.

## Requirements

- A Linux distribution with [Xray] VPN server installed on it.
- Python 3.8 or higher.

## Installation

You can install _PyXrayC_ from [PyPI](https://pypi.org/project/pyxrayc/) using pip:

```bash
$ pip3 install pyxrayc
```

## Usage

You can see _PyXrayC_'s help message by running:

```bash
$ pyxrayc --help
```

## Configuration

_PyXrayC_ uses below environment variables as its configuration:

- `XRAY_CONFIG_PATH`: Path to the config file. Default: `/usr/local/etc/xray/config.json`
- `XRAY_BACKUP_PATH`: Path to the backup file. Default: `/usr/local/etc/xray/backup.json`

## License

This project is licensed under the terms of the [GPL-3.0] licence.

<p align="center">&mdash; ⚡ &mdash;</p>

<!-- Links -->

[GPL-3.0]: https://www.gnu.org/licenses/gpl-3.0.en.html "GNU General Public License v3.0"
[typer]: https://github.com/tiangolo/typer "Typer, build great CLIs. Easy to code. Based on Python type hints."
[xray]: https://github.com/XTLS "Project X"
