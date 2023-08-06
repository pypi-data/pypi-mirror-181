# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['MeowerBot']

package_data = \
{'': ['*']}

install_requires = \
['cloudlink==0.1.7.4', 'requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'meowerbot',
    'version': '2.2.0',
    'description': 'A meower bot lib for py',
    'long_description': '# MeowerBot.py\n\nA bot lib for Meower\n\n\n## License\n\nsee [LICENSE](./LICENSE)\n\n\n## docs\n\nThe Docs are located [here](./docs/callbacks.md)\n\n\n## Quick Example\n\nlook at the [tests directory](./tests) for examples ',
    'author': 'showierdata9978',
    'author_email': '68120127+showierdata9978@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MeowerBots/MeowerBot.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
