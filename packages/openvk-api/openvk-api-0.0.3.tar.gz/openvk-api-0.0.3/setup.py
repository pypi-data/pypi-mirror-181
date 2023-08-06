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
    'version': '0.0.3',
    'description': 'openvk api based on httpx',
    'long_description': '# OpenVk-API\n\nRaw API for [OpenVK](https://github.com/openvk/openvk)\n\n```\npip install openvk-api\n```\n\nUse [OpenVk Docs](https://docs.openvk.su/openvk_engine/api/description/) to use `OpenVkApiMethod`\n\n## Quick example\n\n```python\nfrom openvk_api import OpenVkClient\n# Use token\nclient = OpenVkClient(token="sdflksdfkljssldkjgsdg-jill")\n# Use login and password\nclient = OpenVkClient()\nclient = client.auth_with_password(login="fckptn@gg.su", password="Hydra")\n\napi = client.get_api()\nprint(api.messages.send(user_id=10484, message="Hello, developer"))\n```\n\n## Links\n[Dev\'s OpenVk.uk profile](https://openvk.su/id10484)\n',
    'author': 'NoPlagiarism',
    'author_email': '37241775+NoPlagiarism@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NoPlagiarism/openvk-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
