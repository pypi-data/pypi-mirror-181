# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mc_server_interaction',
 'mc_server_interaction.interaction',
 'mc_server_interaction.manager',
 'mc_server_interaction.utils']

package_data = \
{'': ['*']}

install_requires = \
['aioconsole>=0.5.0,<0.6.0',
 'aiofiles>=22.1.0,<23.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'cached-property>=1.5.2,<2.0.0',
 'mcstatus>=9.4.0,<10.0.0',
 'psutil>=5.9.2,<6.0.0']

setup_kwargs = {
    'name': 'mc-server-interaction',
    'version': '0.3.0',
    'description': 'Module for interacting with Minecraft servers',
    'long_description': '# mc-server-interaction\n\nMC-Server-Interaction is a modern asyncio-based library for interacting with Minecraft servers on your local machine.\n\n## Features\n\n- Modern interface using asyncio and callbacks\n- Manage multiple servers\n    - Create Servers\n    - Start and stop servers\n    - Send commands\n- Retrieve player information\n    - Online players\n    - OP players\n    - Banned players\n    - Whitelisted players\n- Interact with Worlds\n    - Copy worlds from one server to another\n    - Create and restore backups of worlds\n- Monitor system resource usage\n    - CPU\n    - RAM\n\n## Roadmap\n\n- Extend / improve existing features\n- Bukkit servers / easy plugin installation\n- ...\n\n## Requirements\n\n- Python 3.8 minimum\n- [Poetry](https://python-poetry.org/)\n',
    'author': 'Dummerle',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Uncooldevs/mc-server-interaction',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
