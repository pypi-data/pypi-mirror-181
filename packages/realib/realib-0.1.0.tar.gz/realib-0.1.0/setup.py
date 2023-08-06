# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['realib']

package_data = \
{'': ['*']}

install_requires = \
['dash>=2.7.1,<3.0.0', 'pandas>=1.5.2,<2.0.0', 'plotly>=5.11.0,<6.0.0']

setup_kwargs = {
    'name': 'realib',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'swjupudi',
    'author_email': 'swarna.s92@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
