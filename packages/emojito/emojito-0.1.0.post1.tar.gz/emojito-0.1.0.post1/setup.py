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
    'version': '0.1.0.post1',
    'description': 'Define your own shortnames to be replaced with emojis or other content.',
    'long_description': '# Emojito\n\nThere are many packages that provide shortnames for emojis. This package allows you to provide your own shortnames and with what to replace them.\n\n## Features\n\n- Find and replace shortnames. You provide the shortnames and the content with which to replace them. You can also provide a callable from which you can in stead generate the content.\n- Compatible with HTML. In stead of indiscrimnately finding and replacing shortnames anywhere in the text, accidentally replacing content that overlaps with tags, the HTML will be parsed and only the plain text within tags will be affected.\n\n## Example\n\n```py\nfrom emojito import Emojitos\n\n\n# Define your shortnames and their replacements.\nemojitos = Emojitos()\nemojitos.add([\'one\'], \'1️⃣\')\nemojitos.add([\'two\'], \'2️⃣\')\nemojitos.add([\'three\'], \'3️⃣\')\n\n\n# Provide a text containing your shortnames.\ndocument = """\n<h1>This is an example of Emojito</h1>\n\n<ul>\n    <li>:one: Number One</li>\n    <li>:two: Number Two</li>\n    <li>:three: Number Three</li>\n</ul>\n"""\n\n# Replace all instances of your shortnames in the document.\nresult = emojitos.replace(document)\n```',
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
