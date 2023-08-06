# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skate', 'skate.config', 'skate.screens']

package_data = \
{'': ['*']}

install_requires = \
['blessed>=1.19.1,<2.0.0', 'click>=8.1.3,<9.0.0', 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['skate = skate.cli:skate']}

setup_kwargs = {
    'name': 'skate',
    'version': '0.0.4',
    'description': 'Organize and run frequently used commands',
    'long_description': '<p align="center">\n  <img width="460" height="300" src="https://raw.githubusercontent.com/fpgmaas/deptry/main/docs/static/deptry_Logo-01.svg">\n</p>\n\n---\n\n[![Release](https://img.shields.io/github/v/release/fpgmaas/skate)](https://img.shields.io/github/v/release/fpgmaas/skate)\n[![Build status](https://img.shields.io/github/workflow/status/fpgmaas/skate/Main/main)](https://github.com/fpgmaas/skate/actions/workflows/main.yml?query=branch%3Amain)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/skate)](https://pypi.org/project/skate/)\n[![codecov](https://codecov.io/gh/fpgmaas/skate/branch/main/graph/badge.svg)](https://codecov.io/gh/fpgmaas/skate)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/skate)](https://pypistats.org/packages/skate)\n[![License](https://img.shields.io/github/license/fpgmaas/skate)](https://img.shields.io/github/license/fpgmaas/skate)\n\n_skate_ is a command line utility to help you organise and quickly run frequently used commands.\n\n<p align="center">\n<img src="docs/skate.gif"/>\n</p>\n\n## Quickstart\n\n### Installation\n\n_skate_ can be installed by running\n\n```shell\npip install skate\n```\n\nTo get started, run\n\n```shell\nskate init\n```\n\nwhich will prompt to add a `skate/skate.yaml` file in the user\'s home directory for global commands, and/or a `skate.yaml` file in the current directory for commands specific to the current project. \n\nTo use _skate_ to run any of the pre-configured commands, simply run\n\n```\nskate\n```\n\nFor more information, see the [documentation](https://fpgmaas.github.io/skate/).\n\n## Configuration\n\n_skate_ can look for configuration in the following two locations:\n\n- In a `skate.yaml` file in the current directory\n- In any `.yaml` file in the the global configuration directory, which is defaulted to `~/skate`, but which can be overridden with the environment variable `SKATE_HOME`.\n\nAn example `.yaml` file could look as follows:\n\n```yaml\ntest:\n  my-command:\n    cmd: "echo Hello! My name is: $name. My favourite fruit is: $fruit"\n    echo: false\n    args:\n      - name\n      - fruit: apple\n```\n\nWhich adds the command group `test` wth a single command called `my-command`. When `my-command` is selected to be run, _skate_ prompts the user for `name` and `fruit` before running the command specified in `cmd`, where `fruit` is defaulted to `apple` if the user does not give any input.\n\nFor more details, see the [configuration](https://fpgmaas.github.io/skate/configuration) section of the documentation.\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).\n',
    'author': 'Florian Maas',
    'author_email': 'ffpgmaas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fpgmaas/skate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
