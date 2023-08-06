# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_gpt3_codegen']

package_data = \
{'': ['*']}

install_requires = \
['diskcache>=5.4.0,<6.0.0', 'openai>=0.25.0,<0.26.0']

setup_kwargs = {
    'name': 'python-gpt3-codegen',
    'version': '0.1.0',
    'description': 'Auto generate code using openapi.',
    'long_description': None,
    'author': 'Arijit Basu',
    'author_email': 'hi@arijitbasu.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
