# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omars_analysis']

package_data = \
{'': ['*'], 'omars_analysis': ['data/*']}

install_requires = \
['numpy>=1.23.5,<2.0.0', 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'omars-analysis',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Mohammed Saif Ismail Hameed',
    'author_email': 'saifismailh@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
