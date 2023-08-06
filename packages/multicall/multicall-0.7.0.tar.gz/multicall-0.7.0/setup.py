# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multicall']

package_data = \
{'': ['*']}

install_requires = \
['eth_retry>=0.1.8,<0.2.0', 'web3>=5.27,<6.0']

setup_kwargs = {
    'name': 'multicall',
    'version': '0.7.0',
    'description': 'aggregate results from multiple ethereum contract calls',
    'long_description': 'None',
    'author': 'banteg',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
