# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kiera']

package_data = \
{'': ['*']}

install_requires = \
['colored', 'getch', 'requests>=2.28.1', 'rich', 'tomli', 'tomli_w']

entry_points = \
{'console_scripts': ['ka = kiera.main:main', 'kiera = kiera.main:main']}

setup_kwargs = {
    'name': 'kiera',
    'version': '0.0.19',
    'description': '',
    'long_description': '',
    'author': 'Tom Dörr',
    'author_email': 'tomdoerr96@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.3,<4.0',
}


setup(**setup_kwargs)
