# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_poetry_tk']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'test-poetry-tk',
    'version': '0.1.0',
    'description': '',
    'long_description': 'test',
    'author': 'Thomas Kuoch',
    'author_email': 'kuoch.thomas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
