# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['emojito']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0']

setup_kwargs = {
    'name': 'emojito',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Emojito\n\nThere are many packages that provide shortnames for emojis. This package allows you to provide your own shortnames and with what to replace them.\n\n## Features\n\n- Find and replace shortnames. You provide the shortnames and the content with which to replace them.\n- Compatible with HTML. In stead of indiscrimnately finding and replacing shortnames anywhere in the text, accidentally replacing content that overlaps with tags, the HTML will be parsed and only the plain text within tags will be affected.',
    'author': 'Maximillian Strand',
    'author_email': 'maxi@millian.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/deepadmax/emojito',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
