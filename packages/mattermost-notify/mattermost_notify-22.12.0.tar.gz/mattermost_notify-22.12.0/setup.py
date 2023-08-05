# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mattermost_notify', 'tests']

package_data = \
{'': ['*']}

modules = \
['poetry']
install_requires = \
['httpx>=0.23.1,<0.24.0', 'pontos>=22.7.0']

entry_points = \
{'console_scripts': ['mnotify-git = mattermost_notify.git:main']}

setup_kwargs = {
    'name': 'mattermost-notify',
    'version': '22.12.0',
    'description': 'Python tool to post GitHub Action runs to mattermost',
    'long_description': '![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_new-logo_horizontal_rgb_small.png)\n\n# mattermost-notify <!-- omit in toc -->\n\n[![GitHub releases](https://img.shields.io/github/release/greenbone/mattermost-notify.svg)](https://github.com/greenbone/mattermost-notify/releases)\n[![PyPI release](https://img.shields.io/pypi/v/mattermost-notify.svg)](https://pypi.org/project/mattermost-notify/)\n[![code test coverage](https://codecov.io/gh/greenbone/mattermost-notify/branch/main/graph/badge.svg)](https://codecov.io/gh/greenbone/mattermost-notify)\n[![Build and test](https://github.com/greenbone/mattermost-notify/actions/workflows/ci-python.yml/badge.svg)](https://github.com/greenbone/mattermost-notify/actions/workflows/ci-python.yml)\n\nThis tool is desired to post messages to a mattermost channel.\nYou will need a mattermost webhook URL and give a channel name.\n\n## Table of Contents <!-- omit in toc -->\n\n- [Installation](#installation)\n  - [Requirements](#requirements)\n  - [Install using pip](#install-using-pip)\n- [Usage](#usage)\n- [License](#license)\n\n## Installation\n\n### Requirements\n\nPython 3.7 and later is supported.\n\n### Install using pip\n\npip 19.0 or later is required.\n\nYou can install the latest stable release of **mattermost-notify** from the Python\nPackage Index (pypi) using [pip]\n\n    python3 -m pip install --user mattermost-notify\n\n## Usage\n\nPrint a free text message:\n```\nmnotify-git <hook_url> <channel> --free "What a pitty!"\n```\n\nPrint a github workflow status:\n```\nmnotify-git <hook_url> <channel> -S [success, failure] -r <orga/repo> -b <branch> -w <workflow_id> -n <workflow_name>\n```\n\n## License\n\nCopyright (C) 2021-2022 Jaspar Stach\n\nLicensed under the [GNU General Public License v3.0 or later](LICENSE).',
    'author': 'Jaspar Stach',
    'author_email': 'jasp.stac@gmx.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
