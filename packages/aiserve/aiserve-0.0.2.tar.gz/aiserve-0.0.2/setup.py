# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiserve', 'aiserve._internal']

package_data = \
{'': ['*']}

install_requires = \
['bentoml>=1.0.12,<2.0.0',
 'boto3>=1.26.31,<2.0.0',
 'dependency-injector>=4.40.0,<5.0.0',
 'fastapi>=0.88.0,<0.89.0',
 'gitpython>=3.1.29,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pygithub>=1.57,<2.0']

setup_kwargs = {
    'name': 'aiserve',
    'version': '0.0.2',
    'description': '',
    'long_description': '',
    'author': 'Kim Hakhyun',
    'author_email': 'hyun24436@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
