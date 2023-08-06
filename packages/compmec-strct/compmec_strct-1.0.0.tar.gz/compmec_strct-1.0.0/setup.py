# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['strct']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'compmec-strct',
    'version': '1.0.0',
    'description': '',
    'long_description': '[![PyPI Version][pypi-image]][pypi-url]\n[![Build Status][build-image]][build-url]\n[![Code Coverage][coverage-image]][coverage-url]\n[![][versions-image]][versions-url]\n\n# Structures\n\nSolves struture problems using FEM. \n\n* 1D Elements\n    * Cable (Only traction)\n    * Truss (Traction/Compression)\n    * Beam\n        * Euler-Bernoulli\n        * Timoshenko\n* 2D Elements\n    * Plate\n\n## How to use it\n\nThere are many **Python Notebooks** in the folder  ```examples```.\n\nFor simple examples, see\n* 1D Elements\n    * Cable\n    * Truss\n    * Beam\n        * Euler-Bernoulli\n        * Timoshenko\n* 2D Elements\n    * Plate\n\n## Install\n\nThis library is available in [PyPI][pypilink]. To install it\n\n```\npip install compmec-strct\n```\n\nOr install it manually\n\n```\ngit clone https://github.com/compmec/strct\ncd strct\npip install -e .\n```\n\nTo verify if everything works in your machine, type the command in the main folder\n\n```\npytest\n```\n\n## Documentation\n\nIn progress\n\n## Contribute\n\nPlease use the [Issues][issueslink] or refer to the email ```compmecgit@gmail.com```\n\n\n[pypi-image]: https://img.shields.io/pypi/v/compmec-strct\n[pypi-url]: https://pypi.org/project/compmec-strct/\n[build-image]: https://github.com/compmec/strct/actions/workflows/build.yaml/badge.svg\n[build-url]: https://github.com/compmec/strct/actions/workflows/build.yaml\n[coverage-image]: https://codecov.io/gh/compmec/strct/branch/main/graph/badge.svg\n[coverage-url]: https://codecov.io/gh/compmec/strct/\n[versions-image]: https://img.shields.io/pypi/pyversions/compmec-strct.svg?style=flat-square\n[versions-url]: https://pypi.org/project/compmec-strct/\n[pypilink]: https://pypi.org/project/compmec-strct/\n[issueslink]: https://github.com/compmec/strct/issues\n',
    'author': 'Carlos Adir',
    'author_email': 'carlos.adir@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
