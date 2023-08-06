# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tagordo']

package_data = \
{'': ['*']}

install_requires = \
['croniter>=1.3.8,<2.0.0', 'typer[all]>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['tagordo = tagordo.main:app']}

setup_kwargs = {
    'name': 'tagordo',
    'version': '0.1.0',
    'description': 'Tiny python script to check if given checkpoints are up-to-date with a given cron schedule',
    'long_description': '# tagordo\n\n[![PyPI](https://img.shields.io/pypi/v/tagordo)](https://pypi.org/project/tagordo/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tagordo)\n[![PyPI - License](https://img.shields.io/pypi/l/tagordo)](https://github.com/mathiazom/tagordo/blob/main/LICENSE)\n\nTiny python script to check if given checkpoints are up-to-date with a given cron schedule\n\n## `tagordo`\n\nCheck if checkpoints in CHECKPOINTS_DIR are up-to-date with a given CRON_EXPRESSION schedule.\n\n**Usage**:\n\n```console\n$ tagordo [OPTIONS] CRON_EXPRESSION CHECKPOINTS_DIR\n```\n\n**Arguments**:\n\n* `CRON_EXPRESSION`: [required]\n* `CHECKPOINTS_DIR`: [required]\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n',
    'author': 'Mathias O. Myklebust',
    'author_email': 'mathias@oterbust.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mathiazom/tagordo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
