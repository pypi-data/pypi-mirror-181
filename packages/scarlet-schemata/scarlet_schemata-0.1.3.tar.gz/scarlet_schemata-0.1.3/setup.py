# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scarlet_schemata']

package_data = \
{'': ['*']}

install_requires = \
['mock>=4.0.3,<5.0.0',
 'orjson>=3.8.3,<4.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'rich>=12.6.0,<13.0.0']

setup_kwargs = {
    'name': 'scarlet-schemata',
    'version': '0.1.3',
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
