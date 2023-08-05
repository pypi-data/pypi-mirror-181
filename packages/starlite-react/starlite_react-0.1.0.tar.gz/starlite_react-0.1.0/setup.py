# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlite_react']

package_data = \
{'': ['*']}

install_requires = \
['starlite']

entry_points = \
{'console_scripts': ['pytest = pytest:main']}

setup_kwargs = {
    'name': 'starlite-react',
    'version': '0.1.0',
    'description': 'Serve React static files from Starlite',
    'long_description': '# starlite-react\nSmall helper for deploying static files for React with Starlite\n',
    'author': 'Kyle Smith',
    'author_email': 'smithk86@smc3.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/smithk86/starlite-react',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4',
}


setup(**setup_kwargs)
