# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ez_eda', 'ez_eda..ipynb_checkpoints']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.23.5,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'seaborn>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'ez-eda',
    'version': '0.1.0',
    'description': 'simple EDA (Exploratory Data Analysis) visuals',
    'long_description': '',
    'author': 'William VanBuskirk',
    'author_email': 'william.n.vanbuskirk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
