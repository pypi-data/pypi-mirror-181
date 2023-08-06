# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grom', 'grom.progress_bar', 'grom.spin', 'grom.theme']

package_data = \
{'': ['*']}

install_requires = \
['prompt-toolkit>=3.0.36,<4.0.0']

setup_kwargs = {
    'name': 'grom',
    'version': '0.0.1',
    'description': 'A nice set of extensions and stylings for prompt_toolkit',
    'long_description': '# Grom - Delightful command line tools for Python\n\nThese are the early days for Grom. Please check back later...\n',
    'author': 'Jakob Vad Nielsen',
    'author_email': 'jakobvadnielsen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lazee/grom',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
