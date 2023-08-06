# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['value_fetcher']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.27,<2.0.0', 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'value-fetcher',
    'version': '1.0.0',
    'description': 'Fetch a value from various sources, e.g AWS Secrets Manager and SSM Parameter Store',
    'long_description': '# Value fetcher\n## Introduction\nPython module to fetch values from multiple sources including:\n- Environment variables\n- AWS Systems Manager (SSM) Parameter Store\n- AWS Secrets Manager\n',
    'author': 'Voquis Limited',
    'author_email': 'opensource@voquis.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/voquis/value-fetcher',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
