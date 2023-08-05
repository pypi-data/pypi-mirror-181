# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jinjax_ui']

package_data = \
{'': ['*'], 'jinjax_ui': ['components/*']}

install_requires = \
['jinjax>=0.17']

setup_kwargs = {
    'name': 'jinjax-ui',
    'version': '0.1',
    'description': 'Headless JinjaX UI components',
    'long_description': '# JinjaX-UI\n\nHeadless JinjaX UI components\n',
    'author': 'Juan-Pablo Scaletti',
    'author_email': 'juanpablo@jpscaletti.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://jinjax-ui.scaletti.dev/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
