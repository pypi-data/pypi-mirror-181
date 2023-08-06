# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reapermc', 'reapermc.plugins']

package_data = \
{'': ['*'],
 'reapermc': ['modules/*', 'modules/event/*', 'modules/flag/*', 'resources/*']}

install_requires = \
['beet>=0.80.1', 'bolt-expressions>=0.11.0', 'bolt>=0.21.0', 'mecha>=0.61.0']

setup_kwargs = {
    'name': 'reapermc',
    'version': '1.5.0',
    'description': 'A high level framework for the Bolt scripting language.',
    'long_description': "# ReaperMC\n[![GitHub Actions](https://github.com/reapermc/reapermc/workflows/CI/badge.svg)](https://github.com/reapermc/reapermc/actions)\n\n> A high level framework for the Bolt scripting language.\n\n\n\n\n## Introduction\n\nReaper is a framework for the [Bolt](https://github.com/mcbeet/bolt) scripting language. It features complex yet optimized, high level yet simple to use functions.\n\n\nThe goal of this project is to reduce the time developers waste. The aim is to enable developers in creating things faster while focusing on the important bits.\n\nFor further info about the project, check [here](about.md).\n\n## Installation\n\n```bash\npip install reapermc\n```\n\n\n\n## Getting started\n\nThis package is designed to be used within `.bolt` scripts, inside a bolt enabled project. I will never officially support `.mcfunction` files.\n\nTo enable Reaper inside your project, you will need to add `reapermc` to your `require` list inside the beet config file.\n```yaml\nrequire:\n    - bolt\n    - reapermc\n```\n\n\n\nModules named `<namespace>:main` will automatically be the entrypoint.\n\nTo use Reaper's functions, you'll need to import them. (**This won't be necessary in the future**).\n\n```py\n# my_project:main\n\nfrom reapermc:api import sleep, set_time, tag\n\ndef become_wizard():\n    tellraw @s 'You will become a wizard...'\n\n    with sleep(40):\n        set_time(13000)\n        tag('wizardman')\n        tellraw @s 'You are now a wizard!'\n```\n\n\n# Documentation\n\nThe documentation for this project can be found [here](docs/table_of_contents.md).\n\n\n\n---\n\nLicense - [MIT](https://github.com/reapermc/reapermc/blob/main/LICENSE)\n\n",
    'author': 'Yeti',
    'author_email': 'arcticyeti1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/reapermc/reapermc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
