# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycirclize', 'pycirclize.parser', 'pycirclize.utils']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.79,<2.0',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.21.1,<2.0.0',
 'pandas>=1.3.5,<2.0.0']

setup_kwargs = {
    'name': 'pycirclize',
    'version': '0.0.3',
    'description': 'Circular visualization in Python',
    'long_description': '',
    'author': 'moshi4',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://moshi4.github.io/pyCirclize/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
