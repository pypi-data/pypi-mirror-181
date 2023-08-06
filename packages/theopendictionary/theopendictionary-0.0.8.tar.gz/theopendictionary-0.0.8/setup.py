# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['theopendictionary']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'theopendictionary',
    'version': '0.0.8',
    'description': '',
    'long_description': 'None',
    'author': 'Tyler Nickerson',
    'author_email': 'nickersoft@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
