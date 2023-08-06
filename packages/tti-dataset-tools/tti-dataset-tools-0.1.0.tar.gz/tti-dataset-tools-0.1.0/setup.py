# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tti_dataset_tools']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.5,<2.0.0',
 'pandas>=1.1.5,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'shapely>=1.7.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'tti-dataset-tools',
    'version': '0.1.0',
    'description': 'A set of tools for trajectory dataset transformation, clean-up, and augmentation',
    'long_description': '# A set of tools for trajectory dataset transformation, clean-up, and augmentation',
    'author': 'Golam Md Muktadir',
    'author_email': 'muktadir@ucsc.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adhocmaster/TTI-dataset-tools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
