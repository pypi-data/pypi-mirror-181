# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skaha', 'skaha.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1,<2', 'requests>=2,<3', 'toml>=0.10.2,<0.11.0', 'vos>=3,<4']

extras_require = \
{'docs': ['mkdocs-material', 'mkdocstrings-python']}

setup_kwargs = {
    'name': 'skaha',
    'version': '1.1.0',
    'description': 'Python Client for Skaha Container Platform in CANFAR',
    'long_description': 'None',
    'author': 'Shiny Brar',
    'author_email': 'charanjotbrar@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
