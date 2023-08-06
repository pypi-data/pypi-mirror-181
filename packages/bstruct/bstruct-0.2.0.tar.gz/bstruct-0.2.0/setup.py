# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bstruct']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bstruct',
    'version': '0.2.0',
    'description': 'Create efficient encoders and decoders for binary data using type annotations.',
    'long_description': None,
    'author': 'flxbe',
    'author_email': 'flxbe@mailbox.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
