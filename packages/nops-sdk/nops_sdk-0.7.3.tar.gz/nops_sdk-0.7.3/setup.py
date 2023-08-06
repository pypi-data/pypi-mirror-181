# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nops_sdk',
 'nops_sdk._settings',
 'nops_sdk.account',
 'nops_sdk.api',
 'nops_sdk.client',
 'nops_sdk.cloud_infrastructure',
 'nops_sdk.exceptions',
 'nops_sdk.graphql',
 'nops_sdk.k8s',
 'nops_sdk.pricing',
 'nops_sdk.ri']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.21.42,<2.0.0',
 'isort>=5.10.1,<6.0.0',
 'pyflakes>=2.4.0,<3.0.0',
 'pytest>=7.1.1,<8.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'nops-sdk',
    'version': '0.7.3',
    'description': 'SDK for the nOps API',
    'long_description': 'None',
    'author': 'nOps Engineers',
    'author_email': 'eng@nops.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
