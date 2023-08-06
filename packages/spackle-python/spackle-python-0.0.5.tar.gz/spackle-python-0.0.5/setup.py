# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spackle']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.32,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'spackle-python',
    'version': '0.0.5',
    'description': '',
    'long_description': '',
    'author': 'Hunter Clarke',
    'author_email': 'hunter@spackle.so',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
