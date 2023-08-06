# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nb_query']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.2,<2.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['nb-query = nb_query.main:app']}

setup_kwargs = {
    'name': 'nb-query',
    'version': '0.1.0',
    'description': 'Python package to search in jupyter notebooks',
    'long_description': '#nb_query\n\nPython package to search in Jupyter notebooks.\n\n[![Tests](https://github.com/xLaszlo/nb-query/workflows/Tests/badge.svg)](https://github.com/xLaszlo/nb-query/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/xLaszlo/nb-query/branch/master/graph/badge.svg)](https://codecov.io/gh/xLaszlo/nb-query)\n[![PyPI](https://img.shields.io/pypi/v/nb-query.svg)](https://pypi.org/project/nb-query/)\n',
    'author': 'Laszlo Sragner',
    'author_email': 'sragner@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xLaszlo/nb-query',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
