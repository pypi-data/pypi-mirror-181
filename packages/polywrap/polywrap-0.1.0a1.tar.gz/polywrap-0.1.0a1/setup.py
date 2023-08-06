# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polywrap']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'polywrap',
    'version': '0.1.0a1',
    'description': '',
    'long_description': '',
    'author': 'Niraj Kamdar',
    'author_email': 'niraj@polywrap.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
