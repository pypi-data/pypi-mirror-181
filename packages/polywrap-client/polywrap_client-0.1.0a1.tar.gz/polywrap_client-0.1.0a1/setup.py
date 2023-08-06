# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polywrap_client']

package_data = \
{'': ['*']}

install_requires = \
['polywrap-core==0.1.0a1',
 'polywrap-manifest==0.1.0a1',
 'polywrap-msgpack==0.1.0a1',
 'polywrap-result==0.1.0a1',
 'polywrap-uri-resolvers==0.1.0a1',
 'pycryptodome>=3.14.1,<4.0.0',
 'pysha3>=1.0.2,<2.0.0',
 'result>=0.8.0,<0.9.0',
 'unsync>=1.4.0,<2.0.0',
 'wasmtime>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'polywrap-client',
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
