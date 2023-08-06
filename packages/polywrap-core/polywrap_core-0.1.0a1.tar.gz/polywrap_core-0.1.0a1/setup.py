# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polywrap_core',
 'polywrap_core.algorithms',
 'polywrap_core.types',
 'polywrap_core.uri_resolution',
 'polywrap_core.utils']

package_data = \
{'': ['*']}

install_requires = \
['gql==3.4.0',
 'graphql-core>=3.2.1,<4.0.0',
 'polywrap-manifest @ '
 'file:///Users/niraj/Documents/Projects/polywrap/python-client/packages/polywrap-manifest',
 'polywrap-result @ '
 'file:///Users/niraj/Documents/Projects/polywrap/python-client/packages/polywrap-result',
 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'polywrap-core',
    'version': '0.1.0a1',
    'description': '',
    'long_description': 'None',
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
