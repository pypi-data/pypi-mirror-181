# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genhost']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['genhost = genhost.main:main']}

setup_kwargs = {
    'name': 'genhost',
    'version': '0.1.1',
    'description': 'Generate a random hostname based on a wordlist',
    'long_description': '# Genhost\n\nSmall python application to generate hostnames based on a wordlist. Inspired by https://github.com/elasticdog/genhost\n\nThe original wordlist is taken from here, https://web.archive.org/web/20090918202746/http://tothink.com/mnemonic/wordlist.html and there is a version ready to go here in this repo.\n',
    'author': 'Magnus Walbeck',
    'author_email': 'magnus.walbeck@walbeck.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://git.walbeck.it/walbeck-it/genhost',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
