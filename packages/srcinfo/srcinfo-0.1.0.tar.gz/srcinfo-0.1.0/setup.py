# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['srcinfo']

package_data = \
{'': ['*']}

install_requires = \
['parse>=1.19.0,<2.0.0']

entry_points = \
{'console_scripts': ['parse_srcinfo = srcinfo.main:main']}

setup_kwargs = {
    'name': 'srcinfo',
    'version': '0.1.0',
    'description': 'A small library to parse .SRCINFO files',
    'long_description': "================\n python-srcinfo\n================\n\nThis is a small library to easily parse ``.SRCINFO`` files in python, using the python parse_ library.\n\n.. _parse: https://github.com/r1chardj0n3s/parse\n\n\nInstalling\n----------\n\nIf you're on Arch Linux, you can install this library from the [community] repository.\nAlternatively, it can be installed from the PyPI using pip `[1]`__.\n\n.. __: https://pypi.python.org/pypi/srcinfo\n",
    'author': 'Johannes Löthberg',
    'author_email': 'johannes@kyriasis.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
