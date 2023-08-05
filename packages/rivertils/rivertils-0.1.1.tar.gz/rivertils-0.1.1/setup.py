# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rivertils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rivertils',
    'version': '0.1.1',
    'description': '',
    'long_description': "To publish to PyPi you have to pass the creds for pypi\npoetry build\npoetry publish --username(not email) --password\n\n# Rivertils\nScripts that are imported by packages you've deployed to pypi",
    'author': 'Rivers Cuomo',
    'author_email': 'riverscuomo@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
