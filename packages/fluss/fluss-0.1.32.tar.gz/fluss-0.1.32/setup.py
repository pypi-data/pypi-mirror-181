# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fluss', 'fluss.api']

package_data = \
{'': ['*']}

install_requires = \
['rath>=0.3.4']

setup_kwargs = {
    'name': 'fluss',
    'version': '0.1.32',
    'description': '',
    'long_description': 'None',
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
