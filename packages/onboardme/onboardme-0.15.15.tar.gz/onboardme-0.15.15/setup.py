# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onboardme']

package_data = \
{'': ['*'],
 'onboardme': ['config/*',
               'config/firewall/*',
               'config/firewall/ufw/*',
               'config/terminal.sexy/*',
               'scripts/*']}

install_requires = \
['GitPython>=3.1.29,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'click>=8.1.3,<9.0.0',
 'rich>=12.6.0,<13.0.0',
 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['onboardme = onboardme:main']}

setup_kwargs = {
    'name': 'onboardme',
    'version': '0.15.15',
    'description': 'An onboarding tool to install dot files and packages including a default mode with sensible defaults to run on most computers running Debian based distros or macOS.',
    'long_description': '## ☁️  onboard**me** 💻\n\nGet\xa0your\xa0daily\xa0driver\xa0just\xa0the\xa0way\xa0you\xa0like\xa0it,\xa0from\xa0textformatting,\xa0and\xa0dot\xa0files\xa0to\xa0opensource\xa0package\xa0installation,\xa0onboardme\xa0intends to\xa0save\xa0you\xa0time\xa0with\xa0initializing\xa0or\xa0upgrading\xa0your\xa0environment.\n\n### Features\n- manage your [dot files] using a git repo (or use [our default dot files] 😃)\n- install and upgrade libraries and apps\n  - supports different several package managers and a couple of operating systems\n  - can group together packages for different kinds of setups, e.g. gaming, devops, gui\n- easy `yaml` config files in your `$HOME/.config/onboardme/` directory\n\n### Screenshots\n\n[![./docs/onboardme/screenshots/help_text.svg alt=\'screenshot of full output of onboardme --help](https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/help_text.svg)][help text]\n\n<p align="center" width="100%">\nHere\'s an example of the terminal after the script has run:\n</p>\n\n<p align="center" width="100%">\n    <img width="90%" alt="screenshot of terminal after running onboardme. includes colortest-256, powerline prompt, icons for files in ls output, and syntax highlighting examples with cat command." src="https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/terminal_screenshot.png">\n\n</p>\n\n## Quick Start\nThe quickest way to get started on a fresh macOS or distrubtion of Debian (including Ubuntu) is:\n\n```bash\n# this will download setup.sh to your current directory and run it\n/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/jessebot/onboardme/main/setup.sh)"\n\n# this will display the help text for the onboardme cli\nonboardme --help\n```\n\nYou can also read more in depth [Getting Started Docs] 💙!\n\nThere\'s also more [documentation] on basically every program that onboardme touches.\n\n### Upgrading\nIf you\'re on python 3.11, you should be able to do:\n\n```bash\npip3.11 install --upgrade onboardme\n```\n\n## Features\n\n### Made for the following OS (lastest stable):\n\n[![made-for-macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white)](https://wikiless.org/wiki/MacOS?lang=en)\n[![made-for-debian](https://img.shields.io/badge/Debian-A81D33?style=for-the-badge&logo=debian&logoColor=white)](https://www.debian.org/)\n[![made-for-ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)\n\n### Optimized for:\n\n[![made-with-for-vim](https://img.shields.io/badge/VIM-%2311AB00.svg?&style=for-the-badge&logo=vim&logoColor=white)](https://www.vim.org/)\n[![made-with-python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)\n[![made-with-bash](https://img.shields.io/badge/GNU%20Bash-4EAA25?style=for-the-badge&logo=GNU%20Bash&logoColor=white)](https://www.gnu.org/software/bash/)\n\n### Built using these great projects:\n\n[<img src="https://github.com/textualize/rich/raw/master/imgs/logo.svg" alt="rich python library logo with with yellow snake" width="200">](https://github.com/Textualize/rich/tree/master)\n[<img src="https://raw.githubusercontent.com/ryanoasis/nerd-fonts/master/images/nerd-fonts-logo.svg" width="140" alt="nerd-fonts: Iconic font aggregator, collection, and patcher">](https://www.nerdfonts.com/)\n- [powerline](https://powerline.readthedocs.io/en/master/overview.html)\n\n## Status\n\n🎉 Active project! Currently in later alpha :D (*But not yet stable. There be 🐛.*)\n\nPlease report 🐛 in the GitHub issues, and we will collect them,\nand release them into the wild, because we are vegan and nice.\n(Kidding, we will help! 😌)\n\nWe love contributors! Feel free to open a pull request, and we will review it asap! :)\n\n:star: If you like this project, please star it to help us keep motivated :3\n\n### Contributors\n\n<!-- readme: contributors -start -->\n<table>\n<tr>\n    <td align="center">\n        <a href="https://github.com/jessebot">\n            <img src="https://avatars.githubusercontent.com/u/2389292?v=4" width="100;" alt="jessebot"/>\n            <br />\n            <sub><b>JesseBot</b></sub>\n        </a>\n    </td>\n    <td align="center">\n        <a href="https://github.com/cloudymax">\n            <img src="https://avatars.githubusercontent.com/u/84841307?v=4" width="100;" alt="cloudymax"/>\n            <br />\n            <sub><b>Max!</b></sub>\n        </a>\n    </td></tr>\n</table>\n<!-- readme: contributors -end -->\n\n## Shameless plugs for other projects\nLooking for a project to get running on a machine that has no OS at all?\nCheck out [pxeless](https://github.com/cloudymax/pxeless).\n\nActually looking to get started with virtual machines and QEMU?\nCheck out [scrap metal](https://github.com/cloudymax/Scrap-Metal).\n\nLooking for a project to get started with self hosting k8s stuff?\nCheck out [smol k8s lab](https://github.com/jessebot/smol_k8s_lab).\n\n<!-- link references -->\n[documentation]: https://jessebot.github.io/onboardme/onboardme "onboardme documentation"\n[dot files]: https://en.wikipedia.org/wiki/Hidden_file_and_hidden_directory#Unix_and_Unix-like_environments "wiki entry for dot file explanation"\n[our default dot files]: https://github.com/jessebot/dot_files "default dot files for onboardme"\n[help text]: https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/help_text.svg "an svg of the command: onboardme --help"\n[Getting Started Docs]: https://jessebot.github.io/onboardme/onboardme/getting-started "getting started documentation"\n[post screenshot]: https://raw.githubusercontent.com/jessebot/onboardme/main/docs/onboardme/screenshots/terminal_screenshot.png "screenshot of terminal afer onboardme"\n',
    'author': 'Jesse Hitch',
    'author_email': 'jessebot@linux.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://github.com/jessebot/onboardme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
