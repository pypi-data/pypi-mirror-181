# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycodeutils']

package_data = \
{'': ['*']}

install_requires = \
['parse>=1.19.0,<2.0.0']

setup_kwargs = {
    'name': 'pycodeutils',
    'version': '0.0.1',
    'description': 'Utilities for coding challenges.',
    'long_description': '# pycodeutils\nUtilities for coding challenges.\n',
    'author': 'TheRealVizard',
    'author_email': 'vizard@divineslns.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TheRealVizard/pycodeutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
