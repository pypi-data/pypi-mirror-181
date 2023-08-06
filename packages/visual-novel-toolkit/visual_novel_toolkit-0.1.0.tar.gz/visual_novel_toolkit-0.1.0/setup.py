# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['visual_novel_toolkit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'visual-novel-toolkit',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Josiah Kaviani',
    'author_email': 'proofit404@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
