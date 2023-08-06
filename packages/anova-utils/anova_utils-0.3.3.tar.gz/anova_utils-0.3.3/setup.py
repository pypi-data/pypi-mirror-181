# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anova_utils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0', 'pandas>=1.5.2,<2.0.0', 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'anova-utils',
    'version': '0.3.3',
    'description': 'Custom utility functions for conducting ANOVAs (or ANCOVAs).',
    'long_description': 'WIP...\n',
    'author': 'Marcel Wiechmann',
    'author_email': 'mail@mwiechmann.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
