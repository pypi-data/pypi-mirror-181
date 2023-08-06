# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mps_client',
 'mps_client.cli',
 'mps_client.cli.commands',
 'mps_client.core',
 'mps_client.database',
 'mps_client.schema',
 'mps_client.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'httpx>=0.23.0,<0.24.0',
 'matplotlib>=3.6.1,<4.0.0',
 'modelyst-dbgen>=1.0.0a7,<2.0.0',
 'neo4j>=5.3.0,<6.0.0',
 'pandas>=1.5.1,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['mps-client = mps_client.__main__:main']}

setup_kwargs = {
    'name': 'mps-client',
    'version': '0.3.1',
    'description': 'MPS Plotting and CLI Tool',
    'long_description': 'None',
    'author': 'Michael Statt',
    'author_email': 'michael.statt@modelyst.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
