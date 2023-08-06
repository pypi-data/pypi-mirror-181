# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dapla_team_cli',
 'dapla_team_cli.auth',
 'dapla_team_cli.auth.services',
 'dapla_team_cli.doctor',
 'dapla_team_cli.gcp',
 'dapla_team_cli.groups',
 'dapla_team_cli.groups.add_members',
 'dapla_team_cli.groups.list_members',
 'dapla_team_cli.groups.services',
 'dapla_team_cli.secrets',
 'dapla_team_cli.tf',
 'dapla_team_cli.tf.iam_bindings']

package_data = \
{'': ['*'],
 'dapla_team_cli.groups.add_members': ['templates/*'],
 'dapla_team_cli.tf.iam_bindings': ['templates/*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'Jinja2>=3.1.2,<4.0.0',
 'azure-cli>=2.43.0,<3.0.0',
 'click-config-file>=0.6.0,<0.7.0',
 'click-configfile>=0.2.3,<0.3.0',
 'click>=8.1.3',
 'devtools>=0.9.0,<0.10.0',
 'google-cloud-secret-manager>=2.12.4,<3.0.0',
 'jupyterhub>=3.0.0,<4.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'python-tfvars>=0.1.0,<0.2.0',
 'questionary>=1.10.0,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'twine>=4.0.1,<5.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['dpteam = dapla_team_cli.__main__:main']}

setup_kwargs = {
    'name': 'dapla-team-cli',
    'version': '0.0.5',
    'description': 'CLI for working with Dapla Teams',
    'long_description': '# Dapla Team CLI\n\n[![PyPI](https://img.shields.io/pypi/v/dapla-team-cli.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/dapla-team-cli.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/dapla-team-cli)][python version]\n[![License](https://img.shields.io/pypi/l/dapla-team-cli)][license]\n\n[![Tests](https://github.com/statisticsnorway/dapla-team-cli/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/statisticsnorway/dapla-team-cli/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/dapla-team-cli/\n[status]: https://pypi.org/project/dapla-team-cli/\n[python version]: https://pypi.org/project/dapla-team-cli\n[tests]: https://github.com/statisticsnorway/dapla-team-cli/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/statisticsnorway/dapla-team-cli\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\nA CLI for working with Dapla teams.\n\n![dpteam --help](docs/dapla-team-cli-help.png)\n![IAM Bindings](docs/iam-bindings.gif)\n\nFor [installation options see below](#installation), for usage instructions\n[see the manual](https://statisticsnorway.github.io/dapla-team-cli/) or type `--help` on the command line.\n\n<!-- this anchor is linked to, so avoid renaming it -->\n\n## Installation\n\nInstall with [pipx]:\n\n```console\n$ pipx install dapla-team-cli\n```\n\n(Be patient, installation can take some time.)\n\n## Features\n\n- Assign bucket access and GCP roles to members for a limited amount of time\n- Get an overview of a team\'s groups and members\n- Make instant changes to your team\'s access groups, e.g. add a new team member to your team\'s "developers" group.\n- Register team secrets (in a team\'s GCP Secret Manager service)\n- Diagnose your system and get help to install required tooling for easy setup of your development environment\n\n## Links\n\n- [PyPI]\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Dapla Team CLI_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems, please [file an issue] along with a detailed description.\n\n[pypi]: https://pypi.org/project/dapla-team-cli/\n[file an issue]: https://github.com/statisticsnorway/dapla-team-cli/issues\n[pipx]: https://pypa.github.io/pipx\n\n<!-- github-only -->\n\n[license]: https://github.com/statisticsnorway/dapla-team-cli/blob/main/LICENSE\n[contributor guide]: https://github.com/statisticsnorway/dapla-team-cli/blob/main/CONTRIBUTING.md\n[command-line reference]: https://statisticsnorway.github.io/dapla-team-cli/command_reference.md\n',
    'author': 'Kenneth Leine Schulstad',
    'author_email': 'kls@rdck.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/statisticsnorway/dapla-team-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
