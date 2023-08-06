# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'trackable']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.2,<2.0.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['mkdocs==1.3.0',
         'mkdocs-material==8.2.15',
         'mkdocs-include-markdown-plugin>=4.0.3,<5.0.0',
         'mkdocstrings[python]>=0.19.1,<0.20.0'],
 'test': ['black>=21.5b2,<22.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.900,<0.901',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0']}

setup_kwargs = {
    'name': 'trackable',
    'version': '0.1.0',
    'description': 'A minimalistic machine learning model tracker and reporting tool.',
    'long_description': "# trackable\n\n[![pypi](https://img.shields.io/pypi/v/trackable.svg)](https://pypi.org/project/trackable/)\n[![python](https://img.shields.io/pypi/pyversions/trackable.svg)](https://pypi.org/project/trackable/)\n[![Build Status](https://github.com/MillenniumForce/trackable/actions/workflows/dev.yml/badge.svg)](https://github.com/MillenniumForce/trackable/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/MillenniumForce/trackable/branch/main/graphs/badge.svg)](https://codecov.io/github/MillenniumForce/trackable)\n\nA minimalistic machine learning model tracker and reporting tool\n\n* Documentation: <https://MillenniumForce.github.io/trackable>\n* GitHub: <https://github.com/MillenniumForce/trackable>\n* PyPI: <https://pypi.org/project/trackable/>\n* Free software: MIT\n\n`trackable` is a package focussed on users already familiar with machine learning in Python and aims to:\n\n1. Provide a minimal model tracking tool with no frills\n2. An intuitive and lightweight api\n\n## Installation\n\nThe latest released version can be installed from [PyPI](https://pypi.org/project/trackable/) using:\n\n```bash\n# pip\npip install trackable\n```\n\n## Features\n\nTo start using `trackable` import the main reporting functionality via:\n\n```python\nfrom trackable import Report\n```\n\nIt's simple to start using the package. The example below (although simplistic) shows how easy it\nis to pick up the api:\n\n```python\nfrom sklearn.datasets import make_classification\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.metrics import accuracy_score, f1_score, roc_auc_score\nfrom trackable import Report\n\nX, y = make_classification()\n\nlr = LogisticRegression().fit(X, y)\nrf = RandomForestClassifier().fit(X, y)\n\n# Instantiate the report...\nreport = Report(X, y, metrics = [accuracy_score, f1_score, roc_auc_score])\n\n# Add models...\nreport.add_model(lr)\nreport.add_model(rf)\n\n# Generate the report...\nreport.generate()\n```\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n",
    'author': 'Julian Garratt',
    'author_email': 'trackable.py@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MillenniumForce/trackable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
