# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fourier_sine']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fourier-sine',
    'version': '0.2.0',
    'description': 'Fourier Analysis with sine waves',
    'long_description': None,
    'author': 'Andrew Matte',
    'author_email': 'andrew.matte@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
