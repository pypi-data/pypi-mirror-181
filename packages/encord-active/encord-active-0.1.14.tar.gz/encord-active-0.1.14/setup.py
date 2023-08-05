# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['encord_active',
 'encord_active.app',
 'encord_active.app.actions_page',
 'encord_active.app.actions_page.coco_parser',
 'encord_active.app.cli',
 'encord_active.app.common',
 'encord_active.app.common.components',
 'encord_active.app.common.components.sticky',
 'encord_active.app.conf',
 'encord_active.app.data_quality',
 'encord_active.app.data_quality.sub_pages',
 'encord_active.app.db',
 'encord_active.app.model_assertions',
 'encord_active.app.model_assertions.components',
 'encord_active.app.model_assertions.sub_pages',
 'encord_active.app.views',
 'encord_active.lib',
 'encord_active.lib.coco',
 'encord_active.lib.common',
 'encord_active.lib.embeddings',
 'encord_active.lib.metrics',
 'encord_active.lib.metrics.geometric',
 'encord_active.lib.metrics.heuristic',
 'encord_active.lib.metrics.semantic',
 'encord_active.lib.model_predictions']

package_data = \
{'': ['*'], 'encord_active.app': ['assets/*', 'static/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'av>=9.2.0,<10.0.0',
 'encord>=0.1.43,<0.2.0',
 'faiss-cpu>=1.7.2,<2.0.0',
 'inquirer>=2.10.0,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'matplotlib>=3.5.3,<4.0.0',
 'natsort>=8.1.0,<9.0.0',
 'numpy>=1.23.1,<2.0.0',
 'opencv-python==4.5.5.64',
 'pandas>=1.4.3,<2.0.0',
 'plotly>=5.10.0,<6.0.0',
 'psutil>=5.9.4,<6.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'pytz>=2022.2.1,<2023.0.0',
 'rich>=12.6.0,<13.0.0',
 'scikit-learn>=1.0.1,<2.0.0',
 'scipy==1.8.1',
 'screeninfo>=0.8.1,<0.9.0',
 'shapely>=1.7.0,<2.0.0',
 'streamlit-nested-layout>=0.1.1,<0.2.0',
 'streamlit==1.13.0',
 'termcolor>=2.0.1,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'torch>=1.12.1,<2.0.0',
 'torchvision>=0.13.1,<0.14.0',
 'typer>=0.6.1,<0.7.0',
 'types-pytz>=2022.2.1,<2023.0.0',
 'watchdog>=2.1.9,<3.0.0']

extras_require = \
{'coco': ['pycocotools>=2.0.6,<3.0.0']}

entry_points = \
{'console_scripts': ['encord-active = encord_active.app.cli.main:cli']}

setup_kwargs = {
    'name': 'encord-active',
    'version': '0.1.14',
    'description': 'Enable users to improve machine learning models in an active learning fashion via data quality, label quality, and model assertions.',
    'long_description': '<h1 align="center">\n  <p align="center">Encord Active</p>\n  <a href="https://encord.com"><img src="src/encord_active/app/assets/encord_2_02.png" width="150" alt="Encord logo"/></a>\n</h1>\n\n[!["Join us on\nSlack"](https://img.shields.io/badge/Slack-4A154B?logo=slack&logoColor=white)][join-slack] [![Twitter\nFollow](https://img.shields.io/twitter/follow/encord_team?label=%40encord_team&style=social)][twitter-url]\n[![PRs-Welcome][contribute-image]][contribute-url]\n\n## Documentation\n\nPlease refer to our [documentation][encord-active-docs].\n\n## Installation\n\nThe simplest way to install the CLI is using `pip` in a suitable virtual environment:\n\n```shell\npip install encord-active\n```\n\nWe recommend using a virtual environment, such as `venv`:\n\n```shell\n$ python3.9 -m venv ea-venv\n$ source ea-venv/bin/activate\n$ pip install encord-active\n```\n\n> `encord-active` requires [python3.9](https://www.python.org/downloads/release/python-3915/).\n> If you have trouble installing `encord-active`, you find more detailed instructions on\n> installing it [here][encord-active-docs].\n\n## Downloading a pre-built project\n\nThe quickest way to get started is by downloading an existing dataset.\nThe download command will setup a directory where the project will be stored and will ask which pre-built dataset to use.\n\n```shell\n$ encord-active download\n$ encord-active visualise /path/to/project\n```\n\nThe app should automatically open in the browser. If not, navigate to `localhost:8501`.\nOur [Docs][encord-active-docs] contain more information about what you can see in the page.\n\n## Importing an Encord Project\n\nThis section requires setting up an ssh key with Encord, so slightly more technical.\n\n> If you haven\'t set up an ssh key with Encord, you can follow the tutorial in this [link](https://docs.encord.com/admins/settings/public-keys/#set-up-public-key-authentication)\n\nTo import an Encord project, use this script:\n\n```shell\n$ encord-active import project\n```\n\n## Development\n\n### Write your own metrics\n\nEncord Active isn\'t limited to the metrics we provided, it is actually quite easy to write your own 🔧\nSee the [Writing Your Own Metric](https://docs.encord.com/admins/settings/public-keys/#set-up-public-key-authentication) page on the WIKI for details on this.\n\n### Pre-commit hooks\n\nIf you have installed the dependencies with poetry, then you can install pre-commit hooks by running the following command:\n\n```shell\n$ pre-commit install\n```\n\nThe effect of this will be that `black`, `isort`, `mypy`, and `pylint` needs to run without finding issues with the code before you are allowed to commit.\nWhen you commit and either `black` or `isort` fails, committing again is enough, as the side effect of committing the first time is to reformat files.\n\nRunning each of the tools individually on your code can be done as follows:\n\n```shell\n$ poetry run black --config=pyproject.toml .\n$ poetry run isort --sp=pyproject.toml .\n$ poetry run mypy . --ignore-missing-imports\n$ poetry run pylint -j 0 --rcfile pyproject.toml [subdir]\n```\n\n## Community and Support\n\nJoin our community on [Slack][join-slack] and [Twitter][twitter-url]!\n\n[Suggest improvements and report problems][new-issue]\n\n# Contributions\n\nIf you\'re using Encord Active in your organization, please try to add your company name to the [ADOPTERS.md](./ADOPTERS.md). It really helps the project to gain momentum and credibility. It\'s a small contribution back to the project with a big impact.\n\nRead the [contributing docs][contribute-url].\n\n# Licence\n\nThis project is licensed under the terms of the AGPL-3.0 license.\n\n[encord-active-docs]: https://encord-active-docs.web.app/\n[contribute-url]: https://encord-active-docs.web.app/contributing\n[contribute-image]: https://img.shields.io/badge/PRs-welcome-blue.svg\n[join-slack]: https://join.slack.com/t/encordactive/shared_invite/zt-1hc2vqur9-Fzj1EEAHoqu91sZ0CX0A7Q\n[twitter-url]: https://twitter.com/encord_team\n[new-issue]: https://github.com/encord-team/encord-active/issues/new\n',
    'author': 'Cord Technologies Limited',
    'author_email': 'hello@encord.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://encord.com/encord_active/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*, !=3.8.*',
}


setup(**setup_kwargs)
