# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ez_eda', 'ez_eda..ipynb_checkpoints']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.2,<2.0.0', 'seaborn>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'ez-eda',
    'version': '0.1.1',
    'description': 'simple EDA (Exploratory Data Analysis) visuals',
    'long_description': '# ez-eda overview\n- This library is a collection of simplified functions for visualizing dataframes quickly and easily\n- I started this project after needing more refined heatmaps to understanding correlation\n\n## ez correlation plot \n```\nfrom ez_eda import ez_corr_heatmap\n```\nThis function creates a cleaner seaborn-based heatmap to show correlations between numeric features\n',
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
