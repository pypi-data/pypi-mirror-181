# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['state_interface']

package_data = \
{'': ['*']}

install_requires = \
['ase>=3.22,<4.0', 'flake8>=4.0.1,<5.0.0', 'pylint>=2.12.2,<3.0.0']

setup_kwargs = {
    'name': 'state-interface',
    'version': '1.0.0',
    'description': 'ASE STATE interface',
    'long_description': 'None',
    'author': 'Harry Handoko HALIM',
    'author_email': 'harry@cp.prec.eng.osaka-u.ac.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
