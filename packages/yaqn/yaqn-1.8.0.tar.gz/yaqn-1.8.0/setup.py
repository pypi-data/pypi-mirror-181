# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['yaqn']

package_data = \
{'': ['*'], 'yaqn': ['.vscode/*', 'assets/*']}

entry_points = \
{'console_scripts': ['yaqn = yaqn.main:main']}

setup_kwargs = {
    'name': 'yaqn',
    'version': '1.8.0',
    'description': 'A quicknotes app made in python and tkinter.',
    'long_description': '# YAQN - Yet Another Quick Note\n> A fast, easy and OOTB app for taking your notes made in Python.\n\n<img src="https://raw.githubusercontent.com/kutu-dev/yaqn/master/assets/screenshots/app.png" alt="Screenshot of the app" width=542>\n\n## Installation\n```\n> pip install yaqn  # Install from pypi\n> yaqn --check # Run the app and generate the config file\n```\n\n## How to use\nRun the `yaqn` command, it will open the app. To save the note and close the app itself just press `Ctrl + Enter`.\n\n### Open with a keyboard shortcut\nThis can\'t be done automatically by `pip`, please use the correct for your OS:\n- MacOS: Use [Karabiner Elements](https://karabiner-elements.pqrs.org/) and import [this rule](https://github.com/kutu-dev/yaqn/tree/master/assets/karabiner-rules/open-yaqn.json). This should work in any standard python installation, if you a using `pyenv` or similar this rule should be modified manually.\n- Windows: _Too complex too configure unfortunately..._\n- Linux, FreeBSD and others depend of the window manager you\'re using.\n\n## Configuration\nYour configuration file is saved by default in:\n- Unix-like: `~/.config/yaqn/config.toml`\n- Windows: `%AppData%\\yaqn\\config.toml`\n\n### Custom config path\nYou can use your custom path for the config using `--config`:\n```\n> yaqn ---config /path/to/config/directory\n```\n### Check the config file integrity\nThe argument `--check` allows you to create, check and repair the config file, just run the command and it will analyze the config:\n```\n> yaqn --check\n[ INFO ] Check mode -> Config checked and operative\n```\n\n### Configuration structure\nAn ordinary config file looks like this:\n```\nnotes_path = \'/path/to/notes/directory\'\nextension = \'md\'\n```\nAnd this is its structure:\n\n| Parameter | Description |\n| --- | --- |\n| `notes_path` | Define the path to the directory the notes will be saved. You can use the word `default` to point to the generic notes path. |\n| `extension` | Define the extension the notes will be saves. _Remember to **not** put `.` before the extension itself._ |\n| `no_whitespaces` |\xa0Define if YAQN should convert all whitespaces to hyphens `-` in the file name. |\n| `no_uppercase` |\xa0Define if YAQN should convert all uppercase letters to lowercase. |\n| `no_firstline` | Define if YAQN should remove the first line of the note before save it (useful with apps like [ObsidianMD](https://obsidian.md/)). |\n\n### Restore configuration to default\nUse the command `yaqn --restore` to regenerate the configuration with its defaults values.\n\n## Author\n\nCreated with :heart: by [Kutu](https://kutu-dev.github.io/).\n> - GitHub - [kutu-dev](https://github.com/kutu-dev)\n> - Twitter - [@kutu_dev](https://twitter.com/kutu_dev)\n\nLogo of the app created by [vladlucha](https://macosicons.com/#/u/vladlucha) (account deleted unfortunately) in [MacOS Icons](https://macosicons.com/#/).\n',
    'author': 'kutu-dev',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kutu-dev/yaqn',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
