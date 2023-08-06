# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polywrap_msgpack']

package_data = \
{'': ['*']}

install_requires = \
['msgpack>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'polywrap-msgpack',
    'version': '0.1.0a1',
    'description': 'WRAP msgpack encoding',
    'long_description': '',
    'author': 'Cesar',
    'author_email': 'cesar@polywrap.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
