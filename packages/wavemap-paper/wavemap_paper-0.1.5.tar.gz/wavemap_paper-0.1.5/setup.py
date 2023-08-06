# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wavemap_paper']

package_data = \
{'': ['*']}

install_requires = \
['cylouvain>=0.2.2,<0.3.0',
 'ipykernel>=6.19.2,<7.0.0',
 'jupyterlab>=3.5.1,<4.0.0',
 'matplotlib>=3.6.2,<4.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'shap>=0.41.0,<0.42.0',
 'umap-learn>=0.5.3,<0.6.0',
 'xgboost>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'wavemap-paper',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Eric Kenji Lee',
    'author_email': 'erickenjilee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
