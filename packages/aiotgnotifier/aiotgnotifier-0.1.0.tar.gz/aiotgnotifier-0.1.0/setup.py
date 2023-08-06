# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiotgnotifier']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.1,<0.24.0']

setup_kwargs = {
    'name': 'aiotgnotifier',
    'version': '0.1.0',
    'description': 'Notifications via Telegram',
    'long_description': '# aiotgnotifier\nНотификация через мессенджер telegram\n',
    'author': 'Andrey Pochatkov',
    'author_email': 'andrey.pochatkov@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/prin-it/aiotgnotifier',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
