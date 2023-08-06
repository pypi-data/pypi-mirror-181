# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pg_docker']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2>=2.9.5,<3.0.0']

entry_points = \
{'pytest11': ['pg_docker = pg_docker._plugin']}

setup_kwargs = {
    'name': 'pg-docker',
    'version': '0.2.0',
    'description': '',
    'long_description': '',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
