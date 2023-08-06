# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbterd',
 'dbterd.adapters',
 'dbterd.adapters.targets',
 'dbterd.adapters.targets.dbml',
 'dbterd.adapters.targets.dbml.engine',
 'dbterd.adapters.targets.dbml.strategies',
 'dbterd.cli',
 'dbterd.helpers']

package_data = \
{'': ['*']}

modules = \
['README', 'poetry']
install_requires = \
['click>=8.1.3,<9.0.0',
 'dbt-artifacts-parser>=0.2.3,<0.3.0',
 'sql-metadata>=2.6.0,<3.0.0',
 'sqlparse>=0.4.3,<0.5.0']

entry_points = \
{'console_scripts': ['dbterd = dbterd.main:main']}

setup_kwargs = {
    'name': 'dbterd',
    'version': '0.1.3b0',
    'description': 'dbterd is a Command Line Interface (CLI) to convert dbt manifest.json file to diagram file',
    'long_description': None,
    'author': 'Dat Nguyen',
    'author_email': 'datnguyen.it09@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
