# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['basic_return']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'basic-return',
    'version': '0.1.0.10',
    'description': '',
    'long_description': '# basic-return\n\n> Manage function returns with a generic class\n\n[![PyPI version][pypi-image]][pypi-url]\n[![Build status][build-image]][build-url]\n[![GitHub stars][stars-image]][stars-url]\n[![Support Python versions][versions-image]][versions-url]\n\n\n\n## Getting started\n\nYou can [get `basic-return` from PyPI](https://pypi.org/project/basic-return),\nwhich means it\'s easily installable with `pip`:\n\n```bash\npython -m pip install basic-return\n```\n\n\n## Example usage\n\n```python\n\nfrom basic_return.BasicReturn import BasicReturn\ndef function(a, b, c=30, d=50):\n    br = BasicReturn()\n\n    if a < 10:\n        br.status = 10\n        br.message = "param a is less than 10"\n        br.payload = {"something": 123456789}\n        return br\n\n    if b > 20:\n        br.status = -10\n        br.message = "param b is bigger than 20"\n        return br\n\n    br.status = 20\n    br.message = "param a is less than 10"\n    return br\n\nbr = function(10, 20, d=40)\nif br.status < 0:\n    print(br.owner_call)  # function(a=10, b=20, c=30, d=40); this is how the function was called so we can replicate the error\n    raise Exception(f"Something bad happens: [{br.status}] - {br.message}")\n\n\n```\n\n\n\n## Changelog\n\nRefer to the [CHANGELOG.md](https://github.com/henriquelino/basic_return/blob/main/CHANGELOG.md) file.\n\n\n\n<!-- Badges -->\n\n[pypi-image]: https://img.shields.io/pypi/v/basic-return\n[pypi-url]: https://pypi.org/project/basic-return/\n\n[build-image]: https://github.com/henriquelino/basic_return/actions/workflows/build.yaml/badge.svg\n[build-url]: https://github.com/henriquelino/basic_return/actions/workflows/build.yaml\n\n[stars-image]: https://img.shields.io/github/stars/henriquelino/basic_return\n[stars-url]: https://github.com/henriquelino/basic_return\n\n[versions-image]: https://img.shields.io/pypi/pyversions/basic_return\n[versions-url]: https://pypi.org/project/basic_return/\n\n',
    'author': 'henrique lino',
    'author_email': 'henrique.lino97@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/henriquelino/basic_return',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
