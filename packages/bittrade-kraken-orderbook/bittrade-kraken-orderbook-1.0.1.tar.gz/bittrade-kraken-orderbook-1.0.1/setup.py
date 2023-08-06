# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bittrade_kraken_orderbook',
 'bittrade_kraken_orderbook.check',
 'bittrade_kraken_orderbook.compute',
 'bittrade_kraken_orderbook.models',
 'bittrade_kraken_orderbook.models.ccxt']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bittrade-kraken-orderbook',
    'version': '1.0.1',
    'description': '',
    'long_description': None,
    'author': 'mat',
    'author_email': 'matt@techspace.asia',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
