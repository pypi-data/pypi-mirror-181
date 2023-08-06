# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['astream',
 'astream.experimental',
 'astream.experimental.miscutils',
 'astream.integrations',
 'astream.transformers']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'astream',
    'version': '0.7.3',
    'description': '',
    'long_description': 'None',
    'author': 'Pedro Batista',
    'author_email': 'pedrovhb@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
