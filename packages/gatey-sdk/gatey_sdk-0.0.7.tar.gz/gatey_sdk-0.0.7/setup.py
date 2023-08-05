# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gatey_sdk', 'gatey_sdk.integrations', 'gatey_sdk.internal']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'gatey-sdk',
    'version': '0.0.7',
    'description': 'Python client for Gatey (https://gatey.florgon.space)',
    'long_description': 'None',
    'author': 'Florgon Team and Contributors',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
