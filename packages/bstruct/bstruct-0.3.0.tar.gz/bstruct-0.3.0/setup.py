# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bstruct']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'bstruct',
    'version': '0.3.0',
    'description': 'Create efficient encoders and decoders for binary data using type annotations.',
    'long_description': 'None',
    'author': 'flxbe',
    'author_email': 'flxbe@mailbox.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
