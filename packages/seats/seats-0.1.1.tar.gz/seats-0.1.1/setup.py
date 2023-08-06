# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seats',
 'seats.cli',
 'seats.cli.cmdbs',
 'seats.cli.connectors',
 'seats.cli.notebooks',
 'seats.clients',
 'seats.cmdbs',
 'seats.connectors',
 'seats.models']

package_data = \
{'': ['*'], 'seats': ['notebooks/*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['seats = seats.cli.cli:entry_point']}

setup_kwargs = {
    'name': 'seats',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Thiago Takayama',
    'author_email': 'thiago@takayama.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
