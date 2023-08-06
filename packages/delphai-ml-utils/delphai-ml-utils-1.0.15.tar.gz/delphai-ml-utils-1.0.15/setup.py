# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['delphai_ml_utils']

package_data = \
{'': ['*']}

install_requires = \
['azure-storage-blob>=12.14.1,<13.0.0',
 'clean-text[gpl]>=0.6.0,<0.7.0',
 'confuse>=2.0.0,<3.0.0',
 'google>=3.0.0,<4.0.0',
 'goose3>=3.1.12,<4.0.0',
 'grpc_requests>=0.1.6,<0.2.0',
 'gspread>=5.7.1,<6.0.0',
 'justext>=3.0.0,<4.0.0',
 'matplotlib>=3.2.2,<4.0.0',
 'mlcm>=0.0.1,<0.0.2',
 'mylib>=0.0.1,<0.0.2',
 'nltk>=3.7,<4.0',
 'numpy>=1.21.1,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'pysbd>=0.3.4,<0.4.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'seaborn>=0.12.1,<0.13.0',
 'tldextract>=3.4.0,<4.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'trafilatura>=1.4.0,<2.0.0']

extras_require = \
{'config': ['omegaconf>=2.1.0,<3.0.0',
            'memoization>=0.3.1,<0.4.0',
            'python-dotenv>=0.14.0,<0.15.0',
            'kubernetes>=12.0.0,<13.0.0',
            'coloredlogs>=14.0,<15.0',
            'keyring>=21.5.0,<22.0.0',
            'dacite>=1.6.0,<2.0.0',
            'deepmerge>=0.1.0,<0.2.0'],
 'database': ['motor>=2.3.0,<3.0.0'],
 'transformers': ['sentencepiece>=0.1.97,<0.2.0',
                  'sacremoses>=0.0.53,<0.0.54',
                  'nlpaug>=1.1.11,<2.0.0',
                  'protobuf<3.21.0',
                  'transformers[onnx]>=4.24.0,<5.0.0',
                  'torch>=1.12.0,<1.13.0',
                  'torchvision>=0.13.0,<0.14.0',
                  'torchaudio>=0.12.0,<0.13.0']}

setup_kwargs = {
    'name': 'delphai-ml-utils',
    'version': '1.0.15',
    'description': 'A Python package to manage delphai machine learning operations.',
    'long_description': 'None',
    'author': 'ml-team-delphai',
    'author_email': 'ml@delphai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/delphai/delphai-ml-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
