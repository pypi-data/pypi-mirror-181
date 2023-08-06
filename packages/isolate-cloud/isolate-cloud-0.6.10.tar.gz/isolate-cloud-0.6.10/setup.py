# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['isolate_cloud', 'isolate_cloud.auth']

package_data = \
{'': ['*']}

install_requires = \
['auth0-python>=3.24.0,<4.0.0',
 'dill==0.3.5.1',
 'grpcio>=1.50.0,<2.0.0',
 'isolate-proto @ ../isolate_proto',
 'isolate>=0.5.0',
 'requests>=2.28.1,<3.0.0',
 'typer>=0.7.0,<0.8.0',
 'typing-extensions==4.4']

entry_points = \
{'console_scripts': ['isolate-cloud = isolate_cloud.cli:cli']}

setup_kwargs = {
    'name': 'isolate-cloud',
    'version': '0.6.10',
    'description': 'SDK and cli for the fal isolate Cloud service',
    'long_description': '',
    'author': 'Features & Labels',
    'author_email': 'hello@fal.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
