# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mynetwork', 'mynetwork.myip', 'mynetwork.speed']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'hurry-filesize>=0.9,<0.10',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'speedtest-cli>=2.1.3,<3.0.0']

entry_points = \
{'console_scripts': ['mynetwork = mynetwork.cli:main']}

setup_kwargs = {
    'name': 'mynetwork',
    'version': '0.1.2',
    'description': '',
    'long_description': '# MyNetwork CLI\n\n## Usage\n```bash\nUsage: mynetwork [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  ip\n  speed  Speed Group\n```\n\n## Speed Group:\n\n```bash\nUsage: mynetwork speed [OPTIONS] COMMAND [ARGS]...\n\n  Speed Group\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  download\n  upload\n```',
    'author': 'Yogesh Sharma',
    'author_email': 'yks0000@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
