# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_recommending', 'my_recommending.models', 'my_recommending.movielens']

package_data = \
{'': ['*'],
 'my_recommending': ['catboost_info/*',
                     'catboost_info/learn/*',
                     'catboost_info/tmp/*',
                     'configs/*',
                     'configs/sweeps/*']}

install_requires = \
['aenum>=3.1.11,<4.0.0',
 'catboost>=1.1,<2.0',
 'dkoshman-my-tools>=0.1.4,<0.2.0',
 'einops>=0.4.1,<0.5.0',
 'gradio>=3.7,<4.0',
 'implicit>=0.6.1,<0.7.0',
 'ipykernel>=6.19.2,<7.0.0',
 'line-profiler>=4.0.2,<5.0.0',
 'matplotlib>=3.5.0,<3.6.0',
 'numba>=0.56.2,<0.57.0',
 'numpy>=1.22,<2.0',
 'pandas>=1.4.0,<2.0.0',
 'protobuf==3.19.4',
 'pytest>=7.1.3,<8.0.0',
 'pytorch-lightning>=1.6,<1.7',
 'scikit-learn>=1.2.0,<2.0.0',
 'scipy>=1.7,<2.0',
 'shap>=0.41.0,<0.42.0',
 'torch>=1.12.1,<1.13',
 'trash-cli>=0.22,<0.23',
 'wandb>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'my-recommending',
    'version': '0.1.19',
    'description': '',
    'long_description': 'Recommending module with svd, matrix factorization and catboost recommendation models.\n',
    'author': 'DimaKoshman',
    'author_email': 'koshmandk@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
