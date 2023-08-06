# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['social_net_img_classifier']

package_data = \
{'': ['*'], 'social_net_img_classifier': ['data/*', 'models/*']}

install_requires = \
['Pillow==9.1.1',
 'PyMySQL==1.0.2',
 'bertopic==0.12.0',
 'boto3>=1.25.1,<2.0.0',
 'fuzzywuzzy==0.18.0',
 'imblearn>=0.0,<0.1',
 'keras==2.9.0',
 'langid==1.1.6',
 'lightgbm==3.3.2',
 'nltk==3.7',
 'numpy==1.21.3',
 'onnxruntime==1.12.0',
 'openai==0.25.0',
 'optuna==2.10.1',
 'pandas==1.3.2',
 'python-Levenshtein==0.20.5',
 'requests>=2.28.1,<3.0.0',
 'reverse_geocoder==1.5.1',
 'scikit-learn==1.1.1',
 'simpletransformers==0.63.7',
 'six==1.16.0',
 'spacy==3.4.1',
 'tensorflow>=2.1.0rc0,<3.0.0',
 'torch==1.10.1',
 'transformers==4.20.1',
 'wj-social-net-queries>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'social-net-img-classifier',
    'version': '0.6.0',
    'description': '',
    'long_description': 'None',
    'author': 'Gabriel',
    'author_email': 'gabriel@whaleandjaguar.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
