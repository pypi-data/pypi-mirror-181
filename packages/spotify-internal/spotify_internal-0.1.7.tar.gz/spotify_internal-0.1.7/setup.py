# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spotify_internal']

package_data = \
{'': ['*']}

install_requires = \
['librespot>=0.0.7,<0.0.8', 'requests>=2.28.1,<3.0.0', 'spotipy>=2.21.0,<3.0.0']

setup_kwargs = {
    'name': 'spotify-internal',
    'version': '0.1.7',
    'description': 'A Python wrapper around the Spotify Internal API which can let users login with their login creds (and not OAuth)',
    'long_description': 'A Python wrapper around the Spotify Internal API which can let users login with their login creds (and not OAuth)\n',
    'author': 'addyett',
    'author_email': 'g.aditya2048@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
