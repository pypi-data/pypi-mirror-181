# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tonapi']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.1']

setup_kwargs = {
    'name': 'tonapi',
    'version': '0.1.0',
    'description': 'Python SDK for tonapi.io',
    'long_description': '# Python SDK for tonapi.io\n[![PyPI version](https://badge.fury.io/py/tonapi.svg)](https://badge.fury.io/py/tonapi)\n[![Downloads](https://pepy.tech/badge/tonapi/month)](https://pepy.tech/project/tonapi/month)\n[![License: GNU General Public License v3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://opensource.org/licenses/GPL-3.0)\n![visitors](https://visitor-badge.glitch.me/badge?page_id=delpydoc.tonapi.readme&left_color=gray&right_color=blue)\n',
    'author': 'delpydoc',
    'author_email': 'delpydoc@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/delpydoc/tonapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
