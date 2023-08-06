# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['udata_hydra', 'udata_hydra.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiocontextvars>=0.2.2,<0.3.0',
 'aiohttp>=3.8.1,<4.0.0',
 'asyncpg-trek>=0.2.1,<0.3.0',
 'asyncpg>=0.27.0,<0.28.0',
 'boto3>=1.21.21,<2.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'humanfriendly>=10.0,<11.0',
 'marshmallow>=3.14.1,<4.0.0',
 'minicli>=0.5.0,<0.6.0',
 'pandas>=1.3.3,<2.0.0',
 'progressist>=0.1.0,<0.2.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'python-magic>=0.4.25,<0.5.0',
 'redis>=4.1.4,<5.0.0',
 'rq>=1.11.1,<2.0.0',
 'sentry-sdk>=1.11.1,<2.0.0',
 'str2bool>=1.1,<2.0']

entry_points = \
{'console_scripts': ['udata-hydra = udata_hydra.cli:run',
                     'udata-hydra-crawl = udata_hydra.crawl:run']}

setup_kwargs = {
    'name': 'udata-hydra',
    'version': '0.3.0.dev675',
    'description': 'Async crawler and datalake service for data.gouv.fr',
    'long_description': 'None',
    'author': 'Opendata Team',
    'author_email': 'opendatateam@data.gouv.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
