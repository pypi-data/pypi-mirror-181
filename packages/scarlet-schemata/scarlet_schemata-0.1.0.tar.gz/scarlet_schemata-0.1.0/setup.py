# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scarlet_schemata']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'scarlet-schemata',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Scarlet\n\nSchemata for scarlet\n',
    'author': 'Rutger Hartog',
    'author_email': 'r.l.hartog92@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
