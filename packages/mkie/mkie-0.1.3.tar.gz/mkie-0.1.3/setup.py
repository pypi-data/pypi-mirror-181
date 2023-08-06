# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkie', 'mkie.core']

package_data = \
{'': ['*']}

install_requires = \
['click-help-colors==0.9.1',
 'click==8.0.3',
 'colorama>=0.4.6,<0.5.0',
 'importlib-metadata>=4.11.4,<5.0.0']

entry_points = \
{'console_scripts': ['mkie = mkie.__main__:Mkie.cli']}

setup_kwargs = {
    'name': 'mkie',
    'version': '0.1.3',
    'description': 'A useful tool for control clis in terminal.',
    'long_description': '# mkie\n\nA useful tool for control clis in terminal.\n\n## Installation\n\nIf you already know how to install python packages, then you can install it via pip.\n\n```\npip3 install mkie\n```\n\n## Upgrade\n\n```\npip3 install --upgrade mkie\n```\n\n## Features\n\n`mkie` is control clis:\n\n- Git\n  - `gitadd`: Auto add all files to git and ignore submodules.\n  - `gitfetch`: Sort out local branchs.\n  - `gitpull`: Pull latest update from git repo.\n  - `s`: Swap current branch to target branch.\n',
    'author': 'Michael Chou',
    'author_email': 'snoopy02m@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cbb23021/mkie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
