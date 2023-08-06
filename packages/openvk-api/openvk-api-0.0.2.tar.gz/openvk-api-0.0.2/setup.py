# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openvk_api']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.1,<0.24.0']

setup_kwargs = {
    'name': 'openvk-api',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'NoPlagiarism',
    'author_email': '37241775+NoPlagiarism@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
