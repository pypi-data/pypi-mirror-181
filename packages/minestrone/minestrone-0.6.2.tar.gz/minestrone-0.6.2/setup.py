# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minestrone', 'minestrone.element']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0']

extras_require = \
{'docs': ['Sphinx>=4.3.2,<5.0.0',
          'linkify-it-py>=1.0.3,<2.0.0',
          'myst-parser>=0.16.1,<0.17.0',
          'furo>=2021.11.23,<2022.0.0',
          'sphinx-copybutton>=0.4.0,<0.5.0',
          'attrs>=21.4.0,<22.0.0',
          'toml'],
 'html5': ['html5lib==1.1'],
 'lxml': ['lxml==4.9.1']}

setup_kwargs = {
    'name': 'minestrone',
    'version': '0.6.2',
    'description': 'Search, modify, and parse messy HTML with ease.',
    'long_description': '# minestrone\n\nSearch, modify, and parse messy HTML with ease.\n\nDocumentation at https://minestrone.readthedocs.io/.\n',
    'author': 'adamghill',
    'author_email': 'adam@adamghill.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adamghill/minestrone/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
