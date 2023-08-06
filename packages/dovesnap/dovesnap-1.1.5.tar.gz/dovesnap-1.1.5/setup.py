# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dovesnap']

package_data = \
{'': ['*']}

install_requires = \
['docker==6.0.1', 'faucetconfrpc==0.22.45', 'graphviz==0.20.1']

entry_points = \
{'console_scripts': ['graph_dovesnap = dovesnap.graph_dovesnap:main']}

setup_kwargs = {
    'name': 'dovesnap',
    'version': '1.1.5',
    'description': 'graphviz generator of dovesnap networks',
    'long_description': None,
    'author': 'Charlie Lewis',
    'author_email': 'clewis@iqt.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
