# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['knactor']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'dash>=2.7.1,<3.0.0',
 'inflection>=0.5.1,<0.6.0',
 'kopf>=1.36.0,<2.0.0',
 'kubernetes>=25.3.0,<26.0.0',
 'pandas>=1.5.2,<2.0.0',
 'python-box>=6.1.0,<7.0.0',
 'pyzed>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'knactor',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Knactor \n',
    'author': 'Ryan Teoh',
    'author_email': 'ryanteoh01@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
