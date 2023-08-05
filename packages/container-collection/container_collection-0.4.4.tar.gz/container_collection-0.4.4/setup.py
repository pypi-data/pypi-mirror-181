# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['container_collection',
 'container_collection.batch',
 'container_collection.docker',
 'container_collection.fargate',
 'container_collection.manifest',
 'container_collection.template']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.59,<2.0.0',
 'deepdiff>=5.8.1,<6.0.0',
 'docker>=6.0.0,<7.0.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'prefect>=2.6.0,<3.0.0',
 'tabulate>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'container-collection',
    'version': '0.4.4',
    'description': 'Collection of tasks for running containerized models.',
    'long_description': '[![Build Status](https://github.com/bagherilab/container-collection/workflows/build/badge.svg)](https://github.com/bagherilab/container-collection/actions?query=workflow%3Abuild)\n[![Codecov](https://img.shields.io/codecov/c/gh/bagherilab/container-collection?token=OH8080ZFCU)](https://codecov.io/gh/bagherilab/container-collection)\n[![Lint Status](https://github.com/bagherilab/container-collection/workflows/lint/badge.svg)](https://github.com/bagherilab/container-collection/actions?query=workflow%3Alint)\n[![Documentation](https://github.com/bagherilab/container-collection/workflows/documentation/badge.svg)](https://bagherilab.github.io/container-collection/)\n[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n',
    'author': 'Jessica S. Yu',
    'author_email': 'jesyu@uw.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
