# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nmr', 'nmr.types']

package_data = \
{'': ['*']}

install_requires = \
['chess>=1.9.3,<2.0.0',
 'datacls>=4.5.0,<5.0.0',
 'dtyper>=2.0.0,<3.0.0',
 'lat-lon-parser>=1.3.0,<2.0.0',
 'typer>=0.7.0,<0.8.0',
 'xmod>=1.3.2,<2.0.0']

setup_kwargs = {
    'name': 'nmr',
    'version': '0.9.0',
    'description': '🔢 name all canonical things 🔢',
    'long_description': '',
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
