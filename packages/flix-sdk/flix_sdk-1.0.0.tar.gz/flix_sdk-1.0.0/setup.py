# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flix', 'flix.cli', 'flix.lib', 'flix.lib.proto']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'anyio>=3.6.1,<4.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'asyncclick>=8.1.3.2,<9.0.0.0',
 'cryptography>=38.0.4,<39.0.0',
 'grpcio>=1.51.1,<2.0.0',
 'protobuf>=4.21.11,<5.0.0',
 'python-dateutil>=2.8.2,<3.0.0']

entry_points = \
{'console_scripts': ['flix = flix.cli.main:main']}

setup_kwargs = {
    'name': 'flix-sdk',
    'version': '1.0.0',
    'description': 'Python SDK and command-line utilities for Flix',
    'long_description': '# WARNING: These scripts are intended for Flix 6.5 and will not work as intended with earlier versions\n\nThis project aims to provide a fully-featured Python SDK for interacting with Flix,\nalong with a command line utility providing commands for some of the most common actions.\n\n# Installing\n\nInstall the SDK using `pip`:\n```\n$ pip install flix-sdk\n```\nafter which the CLI utility can be accessed as `flix` or `python -m flix`.\n\nAn installation of Python 3.10 or higher is required.\n\n# Usage\n\n## As a command-line utility\n\nThis package comes with a `flix` CLI utility that lets you perform some common actions.\nAt the moment you can use it to perform basic cURL-like requests, as well as to manage webhook.\n\n```\n$ flix --help\nUsage: flix [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -s, --server TEXT    The URL of the Flix server.\n  -u, --username TEXT  The username to authenticate with.\n  -p, --password TEXT  The password to authenticate with.\n  --help               Show this message and exit.\n\nCommands:\n  config        Set default configuration values.\n  contactsheet  Manage contact sheet templates.\n  curl          Perform cURL-like requests to a Flix server.\n  logout        Log out the user from Flix by removing any active access...\n  webhook       Manage webhooks.\n```\n\nTo use the `flix` utility, you should configure what server and credentials to use.\nThis is best done either using environment variables, or the `flix config` command.\n\nTo use environment variables, you need to set the `FLIX_SERVER`, `FLIX_USERNAME`, and `FLIX_PASSWORD` variables:\n```\n$ export FLIX_SERVER=http://localhost:8080\n$ export FLIX_USERNAME=admin\n$ export FLIX_PASSWORD=admin\n$ flix curl /servers\nNot signed in, attempting to authenticate...\n{"servers": ...}\n```\n\nYou can also tell `flix` to remember your information using `flix config`:\n```\n$ flix config -s http://localhost:8080 -u admin -p admin\n$ flix curl /servers\nNot signed in, attempting to authenticate...\n{"servers": ...}\n```\n\nAlternatively, you can provide the information directly to the `flix` command:\n```\n$ flix -s http://localhost:8080 -u admin -p admin curl /servers\nNot signed in, attempting to authenticate...\n{"servers": ...}\n```\n\nIf you do not configure your credentials, `flix` will ask for them when attempting to log in:\n```\n$ flix -s http://localhost:8080 curl /servers\nNot signed in, attempting to authenticate...\nUsername: admin\nPassword:\n{"servers": ...}\n```\n\n## As a library\n\nThis package also comes with an asyncio-based library to help you interact with Flix from your own Python scripts.\nSee the `examples` folder for examples of how to use it.\n\n# Versioning policy\n\nThe Flix SDK follows semantic versioning:\n* The major version is increased if a breaking change is introduced, either at the Flix API level, or in the Flix SDK itself.\n* The minor version is increased if new features are added without breaking existing functionality, with a note in the documentation explaining what Flix version is required for the new features.\n* The patch version is increased if a bug fix is made without changing functionality.\n\nTo ensure that an update will not break existing applications, we recommend specifying a dependency on `flix-sdk` in the form of `^1.2.3` or, equivalently, `>=1.2.3 <2.0.0`.\n\n# Development\n\nThis project makes use of [Poetry](https://python-poetry.org/) for packaging and dependency management.\nYou can install a local development copy along with all dependencies using the `poetry´ command:\n```\n$ pip install poetry\n$ poetry install\n```\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.foundry.com/products/flix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
