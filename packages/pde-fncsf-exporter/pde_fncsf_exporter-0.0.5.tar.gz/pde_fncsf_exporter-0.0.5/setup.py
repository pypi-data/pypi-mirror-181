# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pde_fncsf_exporter',
 'pde_fncsf_exporter.api',
 'pde_fncsf_exporter.interactor',
 'pde_fncsf_exporter.interactor.validator']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'awswrangler>=2.17.0,<3.0.0',
 'click>=8.1.3,<9.0.0',
 'clix>=1.0.8,<2.0.0',
 'pandas>=1.5.0,<2.0.0',
 'pydantic>=1.10.2,<2.0.0']

entry_points = \
{'console_scripts': ['pde_fncsf_exporter = pde_fncsf_exporter.api.cli:cli']}

setup_kwargs = {
    'name': 'pde-fncsf-exporter',
    'version': '0.0.5',
    'description': 'Export the data to the PDE-FNCSF platform',
    'long_description': None,
    'author': 'hugo juhel',
    'author_email': 'juhel.hugo@sciance.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.11',
}


setup(**setup_kwargs)
