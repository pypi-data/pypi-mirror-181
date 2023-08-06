# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fish_databricks_jobs', 'fish_databricks_jobs.services']

package_data = \
{'': ['*']}

install_requires = \
['databricks-cli>=0.17.0,<0.18.0',
 'tabulate>=0.9.0,<0.10.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['fish-databricks-jobs = fish_databricks_jobs.cli:app']}

setup_kwargs = {
    'name': 'fish-databricks-jobs',
    'version': '0.4.2',
    'description': '',
    'long_description': '# fish-databricks-jobs \n\nfish-databricks-jobs is cli and python sdk to handle Jobs for Databricks. e.g assign permissions to multiple jobs. User can filter jobs by job name or tags.  \n\nThe current `databricks-cli`(v0.17.4) has limited functionality on the `jobs` api. e.g it can not assign permission to job. \n\n# installation\n```\n$ pip install fish-databricks-jobs\n```\n# usage\n```\n$ fish-databricks-jobs -h\n\n Usage: fish-databricks-jobs [OPTIONS] COMMAND [ARGS]...\n\n╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ --version             -v        0.3.0                                                                                                            │\n│ --install-completion            Install completion for the current shell.                                                                        │\n│ --show-completion               Show completion for the current shell, to copy it or customize the installation.                                 │\n│ --help                -h        Show this message and exit.                                                                                      │\n╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ list                         List Databricks jobs                                                                                                │\n╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n```\n# config authentication\nfish-databricks-jobs uses same config file as `databricks-cli`. e.g.`~/.databrickscfg` for macOS. Similar for Windows.\n```\n[DEFAULT]\nhost = https://example.cloud.databricks.com\ntoken = dapi41bc0e27d8b91fd8c0144f0a2343504b\n```\n\n\n\n',
    'author': 'Tim Chen',
    'author_email': 'firstim@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
