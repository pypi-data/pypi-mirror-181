# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiocrwaler', 'aiocrwaler.core', 'aiocrwaler.stream']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=8.2.5,<9.0.0',
 'aiocsv>=1.2.3,<2.0.0',
 'aiofiles>=22.1.0,<23.0.0',
 'aiohttp[speedups]>=3.8.3,<4.0.0',
 'aiostream>=0.4.5,<0.5.0',
 'elasticsearch7[async]>=7.17.8,<8.0.0',
 'motor>=3.1.1,<4.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'aiocrwaler',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'JimZhang',
    'author_email': 'zzl22100048@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
