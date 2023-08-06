# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdf_oralia']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.5.0,<2.0.0',
 'pdfplumber>=0.7.4,<0.8.0']

entry_points = \
{'console_scripts': ['pdf-oralia = pdf_oralia.scripts:main']}

setup_kwargs = {
    'name': 'pdf-oralia',
    'version': '0.2.5',
    'description': '',
    'long_description': '',
    'author': 'Bertrand Benjamin',
    'author_email': 'benjamin.bertrand@opytex.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
