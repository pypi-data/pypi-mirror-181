# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['galatasaray']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['galatasaray = galatasaray.cli:main'],
 'galatasaray.plugin': ['galatasaray = galatasaray.cli:main']}

setup_kwargs = {
    'name': 'galatasaray',
    'version': '0.1.5',
    'description': 'Everything about the Galatasaray from cli!',
    'long_description': '# Galatasaray\n\nEverything about the Galatasaray from cli!\n\n## Installation\n\n```shell\n$ pip install galatasaray\n```\n\n## Usage\n\n```shell\n$ galatasaray\n```\n\n![galatasaray](./docs/img/screenshot.png)\n',
    'author': 'Ozcan Yarimdunya',
    'author_email': 'ozcanyd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ozcanyarimdunya/galatasaray',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
