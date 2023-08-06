# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autosbatch', 'tests']

package_data = \
{'': ['*'], 'autosbatch': ['template/*']}

install_requires = \
['rich>=12.6.0,<13.0.0', 'typer>=0.7.0,<0.8.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['mkdocs>=1.3.0,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=8.2.15,<9.0.0',
         'mkdocstrings>=0.16.2,<0.17.0',
         'mkdocs-autorefs>=0.2.1,<0.3.0'],
 'test': ['isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.900,<0.901',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0',
          'black>=22.3.0']}

entry_points = \
{'console_scripts': ['autosbatch = autosbatch.cli:main']}

setup_kwargs = {
    'name': 'autosbatch',
    'version': '0.1.4',
    'description': 'submit hundreds of jobs to slurm automatically.',
    'long_description': '# autosbatch\n\n\n[![pypi](https://img.shields.io/pypi/v/autosbatch.svg)](https://pypi.org/project/autosbatch/)\n[![python](https://img.shields.io/pypi/pyversions/autosbatch.svg)](https://pypi.org/project/autosbatch/)\n[![Build Status](https://github.com/Jianhua-Wang/autosbatch/actions/workflows/dev.yml/badge.svg)](https://github.com/Jianhua-Wang/autosbatch/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/Jianhua-Wang/autosbatch/branch/main/graphs/badge.svg)](https://codecov.io/github/Jianhua-Wang/autosbatch)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n\nsubmit hundreds of jobs to slurm automatically\n\n\n* Documentation: <https://Jianhua-Wang.github.io/autosbatch>\n* GitHub: <https://github.com/Jianhua-Wang/autosbatch>\n* PyPI: <https://pypi.org/project/autosbatch/>\n* Free software: MIT\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'Jianhua Wang',
    'author_email': 'jianhua.mert@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Jianhua-Wang/autosbatch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
