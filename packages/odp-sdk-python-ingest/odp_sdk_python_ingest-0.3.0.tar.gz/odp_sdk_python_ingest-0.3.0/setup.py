# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odp',
 'odp.auth',
 'odp.auth.cdf',
 'odp.auth.odp',
 'odp.auth.prefect',
 'odp.compute',
 'odp.compute.blocks',
 'odp.compute.cli',
 'odp.compute.cli.params',
 'odp.compute.config',
 'odp.compute.deploy',
 'odp.compute.deploy.block',
 'odp.compute.deploy.runtime',
 'odp.compute.deploy.schedule',
 'odp.compute.deploy.storage',
 'odp.compute.flow_state',
 'odp.compute.flow_state.store',
 'odp.compute.metrics',
 'odp.compute.metrics.client',
 'odp.compute.state_handlers',
 'odp.compute.tasks',
 'odp.compute.tasks.cdf',
 'odp.types',
 'odp.utils']

package_data = \
{'': ['*']}

install_requires = \
['azure-common>=1.1.28,<2.0.0',
 'azure-identity>=1.11.0,<2.0.0',
 'azure-keyvault-secrets>=4.6.0,<5.0.0',
 'azure-keyvault>=4.2.0,<5.0.0',
 'azure-storage-blob>=12.13.1,<13.0.0',
 'azure-storage-common>=2.1.0,<3.0.0',
 'click>=8.1.3,<9.0.0',
 'cognite-cdffs>=0.1.0,<0.2.0',
 'cognite-sdk>=4.11.0,<5.0.0',
 'dask-kubernetes>=2022.10.1,<2022.11.0',
 'dask>=2022.11.0,<2022.12.0',
 'decorator>=5.1.1,<6.0.0',
 'docker>=6.0.0,<7.0.0',
 'fsspec>=2022.10.0,<2023.0.0',
 'inflection>=0.5.1,<0.6.0',
 'jinja2==3.0.3',
 'msal-extensions>=1.0.0,<2.0.0',
 'msal>=1.19.0,<2.0.0',
 'prefect-azure[blob]>=0.2.2,<0.3.0',
 'prefect-dask>=0.2.0,<0.3.0',
 'prefect-kv>=0.1.0,<0.2.0',
 'prefect>=2.7.2,<3.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pykube-ng>=22.9.0,<23.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.1,<3.0.0',
 'slugify>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'odp-sdk-python-ingest',
    'version': '0.3.0',
    'description': 'ODP ingest SDK',
    'long_description': '# ODP Ingest SDK\n\n<p align="center">\n    <a href="https://ocean-data-community.slack.com" alt="Slack">\n        <img src="https://img.shields.io/badge/slack-join_community-red.svg?color=0052FF&labelColor=090422&logo=slack" />\n    </a>\n</p>\n\n## Welcome!\n\nINTRO\n\n\n## Setting up developer environment\n\nThis project uses the [Poetry](https://python-poetry.org/) package manager.\nPlease follow the [official](https://python-poetry.org/docs/#installation) documentation for installation details\n\nIn addition to Poetry, this project also uses the package [Poe the Poet](https://github.com/nat-n/poethepoet)\nfor running simple tasks with poetry.\n\nWith Poetry installed, you set up the virtual environment and install the dependencies by excluding **test** \ndependencies using single command:\n\n```shell\npoetry install --without test\n```\n\nInstall all the dependencies only if there is a need to run tests for the `storage/cdffs` using the command below.\n\n```shell\npoetry install\n```\n\nConfigure the pre-commit hooks\n\n```shell\npre-commit install\n```\n',
    'author': 'Thomas Li Fredriksen',
    'author_email': 'thomas.fredriksen@oceandata.earth',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
