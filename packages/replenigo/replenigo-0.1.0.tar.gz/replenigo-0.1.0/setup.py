# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['replenigo']

package_data = \
{'': ['*']}

install_requires = \
['oauthlib>=3.2.2,<4.0.0',
 'pyyaml>=6.0,<7.0',
 'requests-oauthlib>=1.3.1,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'termcolor>=2.1.1,<3.0.0',
 'typer[all]>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['replenigo = replenigo.main:app']}

setup_kwargs = {
    'name': 'replenigo',
    'version': '0.1.0',
    'description': "Script that utilizes Sbanken's Open Banking API to refill accounts to specified balances",
    'long_description': '# replenigo\n\n[![PyPI](https://img.shields.io/pypi/v/replenigo)](https://pypi.org/project/replenigo/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/replenigo)\n[![PyPI - License](https://img.shields.io/pypi/l/replenigo)](https://github.com/mathiazom/replenigo/blob/main/LICENSE)\n\nScript that utilizes Sbanken\'s Open Banking API to refill accounts to specified balances\n\n## Usage\n\n> I recommend you to check out Sbanken\'s [developer portal](https://sbanken.no/bruke/utviklerportalen/) and read the [documentation](https://github.com/Sbanken/api-examples#swagger) for the Sbanken API before using this app\n\n1. Retrieve credentials required to use the API at https://sbanken.no/bruke/utviklerportalen/\n\n2. Install `replenigo`\n```shell\npip install replenigo\n```\n\n3. Use [`replenigo.template.yaml`](replenigo.template.yaml) to create your own `replenigo.yaml` config file with required credentials, source account and refill parameters. Some defaults are provide (see [`replenigo.defaults.yml`](replenigo/replenigo.defaults.yaml)), if not specified in `replenigo.yaml`.\n4. See below for use of the `replenigo` CLI\n\n# `replenigo`\n\nScript that utilizes Sbanken\'s Open Banking API to refill accounts to specified balances\n\n**Usage**:\n\n```console\n$ replenigo [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `refill`: Refill accounts to specified balances\n\n## `replenigo refill`\n\nRefill accounts to specified balances\n\n**Usage**:\n\n```console\n$ replenigo refill [OPTIONS]\n```\n\n**Options**:\n\n* `-c, --config-file FILENAME`: Configurations file  [default: replenigo.yaml]\n* `-r, --reverse-if-above-goal / -R, --no-reverse-if-above-goal`: If refill goal has been exceeded, decide if the surplus should be transferred back to the source account\n* `-m, --transfer-message TEXT`: Message to be displayed in the bank transfer (max 30 chars)\n* `-p, --write-checkpoints / -P, --no-checkpoints`: Enable or disable "checkpointing", which creates an empty checkpoint file on each successful refill\n* `-d, --checkpoints-dir DIRECTORY`: Directory to store checkpoint files\n* `--help`: Show this message and exit.\n',
    'author': 'Mathias Oterhals Myklebust',
    'author_email': 'mathias@oterbust.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mathiazom/replenigo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
