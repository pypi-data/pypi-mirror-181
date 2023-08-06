# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forestadmin',
 'forestadmin.datasource_sqlalchemy',
 'forestadmin.datasource_sqlalchemy.utils']

package_data = \
{'': ['*']}

install_requires = \
['forestadmin-datasource-toolkit>=0.1.0-beta.14,<0.2.0',
 'typing-extensions>=4.2,<5.0',
 'tzdata>=2022.6,<2023.0']

extras_require = \
{':python_version < "3.9"': ['backports.zoneinfo[tzdata]>=0.2.1,<0.3.0']}

setup_kwargs = {
    'name': 'forestadmin-datasource-sqlalchemy',
    'version': '0.1.0b14',
    'description': '',
    'long_description': '',
    'author': 'Valentin Monté',
    'author_email': 'valentinm@forestadmin.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
