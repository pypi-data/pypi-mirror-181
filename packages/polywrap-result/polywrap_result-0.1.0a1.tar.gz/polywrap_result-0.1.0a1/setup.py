# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polywrap_result']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'polywrap-result',
    'version': '0.1.0a1',
    'description': 'Result object',
    'long_description': '',
    'author': 'Danilo Bargen',
    'author_email': 'mail@bargen.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
