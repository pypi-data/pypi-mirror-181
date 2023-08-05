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
    'version': '0.1.0',
    'description': '',
    'long_description': '',
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
