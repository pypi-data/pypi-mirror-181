# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lmdemo']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['lm_demo = lmdemo:__main__.main']}

setup_kwargs = {
    'name': 'lmdemo',
    'version': '1.1.0',
    'description': 'A package demonstrating how to package python projects',
    'long_description': '================================================================================\nIntroduction\n================================================================================\n\nThis is a package which shows how to use poetry',
    'author': 'chase mateusiak',
    'author_email': 'chase.mateusiak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cmatKhan/lmdemo',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
