# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smtoolkit', 'smtoolkit.sklearn']

package_data = \
{'': ['*']}

install_requires = \
['pre-commit>=2.20.0,<3.0.0', 'sagemaker==2.124.0']

setup_kwargs = {
    'name': 'sagemaker-mlops-toolkit',
    'version': '0.1.0.dev1',
    'description': 'A short description of the package.',
    'long_description': '',
    'author': 'Ernane Sena',
    'author_email': 'ernane.sena@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1',
}


setup(**setup_kwargs)
