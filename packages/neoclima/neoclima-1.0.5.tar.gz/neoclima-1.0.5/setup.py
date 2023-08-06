# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neoclima']

package_data = \
{'': ['*']}

install_requires = \
['emoji>=2.2.0,<3.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.1,<3.0.0',
 'tinydb>=4.7.0,<5.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['neoclima = neoclima.main:app']}

setup_kwargs = {
    'name': 'neoclima',
    'version': '1.0.5',
    'description': 'Modern CLI Weather App',
    'long_description': '# neoclima\n\n![image](https://img.shields.io/pypi/pyversions/neoclima?color=brightgreen)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n\nModern CLI Weather App\n\n\n## Installation\n\n```python\n  pip install neoclima\n```\n\n## Usage\n\n```python\n  neoclima add nyc # add new city with chosen nickname\n  neoclima now nyc # current weather for nyc\n  neoclima edit nyc # edit city nickname\n  neoclima rm nyc # remove nyc from cities list\n  neoclima ls # list added cities\n```\n\n## Stack\n\n```python\n  Typer & TinyDB\n```\n',
    'author': 'caiopeternela',
    'author_email': 'caiopeternela.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
