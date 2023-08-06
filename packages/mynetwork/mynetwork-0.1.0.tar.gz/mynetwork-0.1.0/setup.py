# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mynetwork', 'mynetwork.myip']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['mynetwork = mynetwork.cli:main']}

setup_kwargs = {
    'name': 'mynetwork',
    'version': '0.1.0',
    'description': '',
    'long_description': 'install dep: poetry install\nupdate dep: poetry update\nadd dep: poetry add click requests\nshow dep: poetry show\nremove dep: poetry remove pendulum\n\nbuild: poetry build\n\ncache list: poetry cache list\n\nVEnv: poetry env info',
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
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
