# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fluid', 'fluid.github', 'fluid.scheduler']

package_data = \
{'': ['*']}

install_requires = \
['aio-kong>=2.8.0,<3.0.0',
 'aio-openapi>=3.1.1,<4.0.0',
 'aiobotocore[boto3]>=2.4.1,<2.5.0',
 'aioconsole>=0.5.0,<0.6.0',
 'aiohttp_cors>=0.7.0,<0.8.0',
 'colorlog>=6.6.0,<7.0.0',
 'inflection>=0.5.1,<0.6.0',
 'prometheus-async>=22.1.0,<23.0.0',
 'pycountry>=22.3.5,<23.0.0',
 'python-json-logger>=2.0.2,<3.0.0',
 'python-slugify[unidecode]>=6.1.0,<7.0.0',
 'redis>=4.4.0,<5.0.0',
 's3fs>=2022.8.2,<2023.0.0',
 'ujson>=5.1.0,<6.0.0',
 'uvloop>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'aio-fluid',
    'version': '0.5.0',
    'description': 'Tools for backend python services',
    'long_description': '# Tools for backend python services\n\n[![PyPI version](https://badge.fury.io/py/aio-fluid.svg)](https://badge.fury.io/py/aio-fluid)\n[![Python versions](https://img.shields.io/pypi/pyversions/aio-fluid.svg)](https://pypi.org/project/aio-fluid)\n[![build](https://github.com/quantmind/fluid/workflows/build/badge.svg)](https://github.com/quantmind/aio-fluid/actions?query=workflow%3Abuild)\n[![codecov](https://codecov.io/gh/quantmind/aio-fluid/branch/master/graph/badge.svg?token=81oWUoyEVp)](https://codecov.io/gh/quantmind/aio-fluid)\n\n## Installation\n\nThis is a simple python package you can install via pip:\n\n```\npip install aio-fluid\n```\n\n## Modules\n\n### [scheduler](./fluid/scheduler)\n\nA simple asynchronous task queue with a scheduler\n\n### [kernel](./fluid/kernel)\n\nAsync utility for executing commands in sub-processes\n\n## AWS\n\npackages for AWS interaction are installed via\n\n- [aiobotocore](https://github.com/aio-libs/aiobotocore)\n- [s3fs](https://github.com/fsspec/s3fs) (which depends on aiobotocore and therefore versions must be compatible)\n- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) is installed as extra dependency of aiobotocore so versioning is compatible\n',
    'author': 'Luca',
    'author_email': 'luca@quantmind.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4',
}


setup(**setup_kwargs)
