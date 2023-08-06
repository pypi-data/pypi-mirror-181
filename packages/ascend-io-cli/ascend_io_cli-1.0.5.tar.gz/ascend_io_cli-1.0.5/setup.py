# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ascend_io_cli', 'ascend_io_cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'ascend-io-sdk>=0.2.52,<0.3.0',
 'pipdeptree>=2.3.1,<3.0.0',
 'rich>=12.5.0,<13.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'tomlkit>=0.11.4,<0.12.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['ascend = ascend_io_cli.cli:app']}

setup_kwargs = {
    'name': 'ascend-io-cli',
    'version': '1.0.5',
    'description': 'The Ascend CLI',
    'long_description': '=====================\nAscend.io CLI\n=====================\n\nThis package contains the `Ascend CLI <https://developer.ascend.io/docs/python-sdk>`_. The\nCLI is designed to make working with the Ascend.io platform simple and easy. This CLI\nwraps the `Ascend Python SDK <https://developer.ascend.io/docs/python-sdk>`_.\n\nGet help by passing ``--help`` into any command for a rundown of the syntax for each command.::\n\n ascend --help\n\nMake sure you are running the most current version::\n\n ascend version\n\nThe CLI can save default values for certain parameters. For example, to set a default hostname::\n\n ascend config set hostname my-ascendhost.company.io\n\nRemoving a default is as simple as::\n\n ascend config unset hostname\n\n---------------\nAuthentication\n---------------\nYou will want to download your API key from the Ascend UI. [Here is some documentation](https://developer.ascend.io/docs/python-sdk#getting-started)\nthat shows you how to get your key. Please keep your key secure!\n\n\n---------------\nRead the Docs\n---------------\n* `Ascend.io Python SDK Documentation <https://developer.ascend.io/docs/python-sdk>`_\n* `Ascend Developer Hub <https://developer.ascend.io>`_\n* `Ascend.io <https://www.ascend.io>`_\n',
    'author': 'Ascend.io Engineering',
    'author_email': 'support@ascend.io',
    'maintainer': 'Ascend.io Engineering',
    'maintainer_email': 'support@ascend.io',
    'url': 'https://www.ascend.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
