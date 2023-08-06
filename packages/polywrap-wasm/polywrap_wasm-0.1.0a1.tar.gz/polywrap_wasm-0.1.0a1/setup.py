# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polywrap_wasm', 'polywrap_wasm.types']

package_data = \
{'': ['*'], 'polywrap_wasm': ['example-wasm-files/*']}

install_requires = \
['polywrap-core==0.1.0a1',
 'polywrap-manifest==0.1.0a1',
 'polywrap-msgpack==0.1.0a1',
 'polywrap-result==0.1.0a1',
 'unsync>=1.4.0,<2.0.0',
 'wasmtime>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'polywrap-wasm',
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
