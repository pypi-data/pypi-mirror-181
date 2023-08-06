# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['melpoi', 'melpoi.scraping.website-monitor', 'melpoi.sql']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.20.1,<0.21.0',
 'ipython>=8.6.0,<9.0.0',
 'opencv-python>=4.6.0.66,<5.0.0.0',
 'selenium>=4.6.0,<5.0.0']

setup_kwargs = {
    'name': 'melpoi',
    'version': '0.1.2',
    'description': '',
    'long_description': '# melpoi\n[![PyPI Latest Release](https://img.shields.io/pypi/v/melpoi.svg)](https://pypi.org/project/melpoi/)\n[![Latest Build](https://github.com/la0bing/melpoi/actions/workflows/ci.yml/badge.svg)](https://github.com/la0bing/melpoi/actions/workflows/release.yml/badge.svg)\n\nmelpoi is a repository with some of the scripts me myself personally find useful. They can be a simple ETL script or even a web scraping script. This is mainly for me to have a centralized place to look for scripts that I need. Feel free to use them if they can help you, you can also submit a pull request to add new things into this that you feel others might benefit from it.\n\n# Categories\n- [Scraping](https://github.com/la0bing/melpoi/tree/master/melpoi/scraping)\n- [SQL](https://github.com/la0bing/melpoi/tree/master/melpoi/sql)\n',
    'author': 'Melvin Low',
    'author_email': 'la0bing07148@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
