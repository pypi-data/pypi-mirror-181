# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lorem_pysum']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'lorem-pysum',
    'version': '0.7.0',
    'description': 'Library to generate instances of Pydantic models.',
    'long_description': '<!--suppress HtmlDeprecatedAttribute -->\n<div align=center>\n  <h1>Lorem Pysum</h1>\n  <h3>Library to generate instances of Pydantic models..</h3>\n  <img src="https://img.shields.io/badge/License-MIT-blue.svg"\n   height="20"\n   alt="License: MIT">\n  <img src="https://img.shields.io/badge/code%20style-black-000000.svg"\n   height="20"\n   alt="Code style: black">\n  <img src="https://img.shields.io/pypi/v/lorem-pysum.svg"\n   height="20"\n   alt="PyPI version">\n  <img src="https://img.shields.io/badge/coverage-100%25-success"\n   height="20"\n   alt="Code Coverage">\n</div>\n\n## Install\n\nLorem Pysum is on PyPI and can be installed with:\n\n```shell\npoetry add lorem-pysum\n```\n\nor\n\n```shell\npip install lorem-pysum\n```\n\n## Usage\n\nGiven a Pydantic model type Lorem Pysum can generate instances of that model with\nrandomly generated values.\n\n## Example\n\n```python\nfrom enum import auto, Enum\nfrom uuid import UUID\n\nimport lorem_pysum\nfrom pydantic import BaseModel\n\n\nclass Flavor(Enum):\n    MOCHA = auto()\n    VANILLA = auto()\n\n\nclass Brand(BaseModel):\n    brand_name: str\n\n\nclass Coffee(BaseModel):\n    id: UUID\n    description: str\n    cream: bool\n    sweetener: int\n    flavor: Flavor\n    brand: Brand\n\n\nlorem_pysum.generate(Coffee)\n# Result -> Coffee(id=UUID(\'6cbe3fef-3617-4536-a8af-842221d4105b\'), description=\'laboris\', cream=True, sweetener=27, flavor=<Flavor.VANILLA: 2>, brand=Brand(brand_name=\'non\'))\n```\n',
    'author': 'Matthew Burkard',
    'author_email': 'matthewjburkard@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mburkard/lorem-pysum',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
