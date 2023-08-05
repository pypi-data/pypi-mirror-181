# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jeeves_yeti_pyproject']

package_data = \
{'': ['*']}

install_requires = \
['flakeheaven>=3.2.1,<4.0.0',
 'jeeves-shell>=2.0.1,<3.0.0',
 'mypy>=0.910,<0.911',
 'plumbum>=1.8.0,<2.0.0',
 'pytest-cov>=2.12,<3.0',
 'pytest-randomly>=3.8,<4.0',
 'pytest>=6.2,<7.0',
 'rich>=12.6.0,<13.0.0',
 'safety>=1.10,<2.0',
 'tomlkit>=0.11.6,<0.12.0',
 'wemake-python-styleguide>=0.17.0,<0.18.0']

entry_points = \
{'jeeves': ['pyproject = jeeves_yeti_pyproject:jeeves']}

setup_kwargs = {
    'name': 'jeeves-yeti-pyproject',
    'version': '0.1.0',
    'description': 'Opinionated Jeeves plugin for Python projects.',
    'long_description': '',
    'author': 'Anatoly Scherbakov',
    'author_email': 'altaisoft@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
