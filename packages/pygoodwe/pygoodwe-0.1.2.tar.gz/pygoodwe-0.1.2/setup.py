# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygoodwe']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pygoodwe',
    'version': '0.1.2',
    'description': 'A command line tool and python library to query the GOODWE SEMS Portal APIs.',
    'long_description': '\n# pygoodwe\n\nA command line tool and python library to query the GOODWE SEMS Portal APIs.\n\n## API Docs\n\nAuto-generated documentation is here: https://yaleman.github.io/pygoodwe/\n\n## Installation\n\nYou need to have Python 3 and pip installed. Then:\n\n    python -m pip install pygoodwe\n\nDetermine the Station ID from the GOODWE site as follows. Open the [Sems Portal](https://www.semsportal.com). The Plant Status will reveal the Station ID in the URL. Example:\n\n    https://www.semsportal.com/powerstation/powerstatussnmin/11112222-aaaa-bbbb-cccc-ddddeeeeeffff\n\nThen the Station ID is `11112222-aaaa-bbbb-cccc-ddddeeeeeffff`.\n\n## Contributions\n\nPlease feel free to lodge an [issue or pull request on GitHub](https://github.com/yaleman/pygoodwe/issues).\n\n## Thanks\n\n* Originally based off the work of [Mark Ruys and his gw2pvo software](https://github.com/markruys/gw2pvo) - I needed something more flexible, so I made this.\n\n## Disclaimer\n\nGOODWE access is based on the undocumented API used by mobile apps. This could break at any time.\n\n## Example Code\n\nPlease check out test.py in the base of the repository for some simple example code.\n',
    'author': 'James Hodgkinson',
    'author_email': 'james@terminaloutcomes.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
