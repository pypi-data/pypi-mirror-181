# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipfnetcfgbu', 'ipfnetcfgbu.cli', 'ipfnetcfgbu.vcs']

package_data = \
{'': ['*']}

install_requires = \
['aio-ipfabric>=1.0.0,<2.0.0',
 'aiofiles>=22.1.0,<23.0.0',
 'click>=8.1.3,<9.0.0',
 'first>=2.0.2,<3.0.0',
 'maya>=0.6.1,<0.7.0',
 'pexpect>=4.8.0,<5.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['ipf-netcfgbu = ipfnetcfgbu.cli.main:run']}

setup_kwargs = {
    'name': 'ipf-netcfgbu',
    'version': '1.0.0',
    'description': 'Network Config Backup from IP Fabric to Git',
    'long_description': 'None',
    'author': 'Jeremy Schulman',
    'author_email': 'nwkautomaniac@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
