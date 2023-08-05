# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nosql', 'taskqueue', 'zync']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.1,<2.0.0',
 'pymongo>=4.3.2,<5.0.0',
 'redis>=4.3.4,<5.0.0',
 'rq>=1.11.1,<2.0.0']

setup_kwargs = {
    'name': 'pyzync',
    'version': '0.1.0',
    'description': 'An integration framework for continuously syncing data',
    'long_description': 'None',
    'author': 'Joseph DeWitt',
    'author_email': 'joseph@zync.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
