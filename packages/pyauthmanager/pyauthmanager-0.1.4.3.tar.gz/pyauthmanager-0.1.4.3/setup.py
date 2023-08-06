# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyauthmanager',
 'pyauthmanager.aws',
 'pyauthmanager.azure',
 'pyauthmanager.gcp',
 'pyauthmanager.libs']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.32,<2.0.0',
 'botocore>=1.29.32,<2.0.0',
 'firebase-admin>=6.0.1,<7.0.0',
 'python-decouple>=3.6,<4.0',
 'python-jose>=3.3.0,<4.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pyauthmanager',
    'version': '0.1.4.3',
    'description': '',
    'long_description': '# py-auth-manager\n\n',
    'author': 'Touni Atchadé',
    'author_email': 'romuald.atchade@tounilab.com>, Hervé Martin <hervefranciscomartin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
