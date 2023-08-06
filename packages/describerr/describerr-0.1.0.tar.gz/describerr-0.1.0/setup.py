# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['describerr']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'describerr',
    'version': '0.1.0',
    'description': 'Simple Opinionated git log to a changelog',
    'long_description': 'None',
    'author': 'Krzysztof Czeronko',
    'author_email': 'krzysztof.czeronko@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
