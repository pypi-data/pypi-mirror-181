# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openrlbenchmark']

package_data = \
{'': ['*']}

install_requires = \
['expt>=0.4.1,<0.5.0',
 'importlib-metadata>=5.1.0,<6.0.0',
 'multiprocess>=0.70.13,<0.71.0',
 'pip>=22.1.2,<23.0.0',
 'rich>=12.6.0,<13.0.0',
 'seaborn>=0.12.1,<0.13.0',
 'tabulate>=0.9.0,<0.10.0',
 'tueplots>=0.0.4,<0.0.5',
 'wandb>=0.13.7,<0.14.0']

setup_kwargs = {
    'name': 'openrlbenchmark',
    'version': '0.1.1a0',
    'description': '',
    'long_description': 'None',
    'author': 'Costa Huang',
    'author_email': 'costa.huang@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
