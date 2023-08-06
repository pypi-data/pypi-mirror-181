# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polywrap_uri_resolvers',
 'polywrap_uri_resolvers.abc',
 'polywrap_uri_resolvers.cache',
 'polywrap_uri_resolvers.errors',
 'polywrap_uri_resolvers.helpers',
 'polywrap_uri_resolvers.legacy',
 'polywrap_uri_resolvers.types']

package_data = \
{'': ['*']}

install_requires = \
['polywrap-core==0.1.0a1',
 'polywrap-result==0.1.0a1',
 'polywrap-wasm==0.1.0a1',
 'wasmtime>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'polywrap-uri-resolvers',
    'version': '0.1.0a1',
    'description': '',
    'long_description': 'TODO',
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
