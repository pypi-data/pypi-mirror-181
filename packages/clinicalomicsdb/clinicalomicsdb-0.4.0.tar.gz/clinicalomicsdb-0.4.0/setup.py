# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clinicalomicsdb']

package_data = \
{'': ['*']}

install_requires = \
['Werkzeug>=2.1.2,<3.0.0',
 'bs4>=0.0.1,<0.0.2',
 'pandas>=1.4.3,<2.0.0',
 'requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'clinicalomicsdb',
    'version': '0.4.0',
    'description': 'Clinical Trial Omics Database for machine learning benchmarking',
    'long_description': None,
    'author': 'Chang In Moon',
    'author_email': 'moonchangin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
