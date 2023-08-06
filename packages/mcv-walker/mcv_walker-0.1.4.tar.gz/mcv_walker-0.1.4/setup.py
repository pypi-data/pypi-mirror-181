# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcv_walker']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.5,<2.0.0', 'pynput>=1.7.6,<2.0.0', 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['mcv_walker = mcv_walker.main:main']}

setup_kwargs = {
    'name': 'mcv-walker',
    'version': '0.1.4',
    'description': '',
    'long_description': 'A quickly thrown together tool to keep track of a grid exploration system.',
    'author': 'Greg Olmschenk',
    'author_email': 'greg@olmschenk.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
