# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bittrade_kraken_rest',
 'bittrade_kraken_rest.connection',
 'bittrade_kraken_rest.endpoints',
 'bittrade_kraken_rest.endpoints.private',
 'bittrade_kraken_rest.endpoints.public',
 'bittrade_kraken_rest.environment',
 'bittrade_kraken_rest.exceptions',
 'bittrade_kraken_rest.models',
 'bittrade_kraken_rest.models.private',
 'bittrade_kraken_rest.models.public']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

extras_require = \
{'fire': ['rich>=12.6.0,<13.0.0', 'fire>=0.5.0,<0.6.0']}

setup_kwargs = {
    'name': 'bittrade-kraken-rest',
    'version': '0.9.0',
    'description': 'Kraken REST library with an optional CLI',
    'long_description': None,
    'author': 'Matt Kho',
    'author_email': 'matt@techspace.asia',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
