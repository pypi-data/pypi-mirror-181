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
    'version': '0.1.1',
    'description': 'Python package to search in jupyter notebooks',
    'long_description': '# nb_query\n\nPython package to search in Jupyter notebooks.\n\n[![Tests](https://github.com/xLaszlo/nb-query/workflows/Tests/badge.svg)](https://github.com/xLaszlo/nb-query/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/xLaszlo/nb-query/branch/master/graph/badge.svg)](https://codecov.io/gh/xLaszlo/nb-query)\n[![PyPI](https://img.shields.io/pypi/v/nb-query.svg)](https://pypi.org/project/nb-query/)\n[![Read the Docs](https://readthedocs.org/projects/nb-query/badge/)](https://nb-query.readthedocs.io/)\n\nInstallation:\n\n```\n    $ pip install nb-query\n```\n\nUsage\n\n```\n    >>  from nb_query import nb_query\n    >>  nb_query(\'Hello\')\n    >>  nb_query(\'Hello\', [\'data/notebooks\',])\n    >>  nb_query(\'He(ll|r)o\')\n    >>  nb_query(lambda line: len(line) == 2)\n```\n\nCreated with the help of the "Hypermodern python" article series.\n\nJoin the [Code Quality for Data Science (CQ4ds) Discord channel](https://discord.com/invite/8uUZNMCad2) for feedback.\n',
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
