# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mum']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['mum = mum.cli:mum']}

setup_kwargs = {
    'name': 'pymum',
    'version': '0.3.0',
    'description': 'Save your weekly progress.',
    'long_description': '## mum\n\nA simple tool to help you keep track of your work throughout the week, it also helps you\nkeep track of short-term todo stuff. It will remind you during the week so you don\'t\nhave to think about it. Just like mums do to little kids :)\n\n## Table of contents\n\n<!-- toc -->\n\n- [Requirements](#requirements)\n- [Installation](#installation)\n- [Usage](#usage)\n\n<!-- tocstop -->\n\n### Requirements\n\n- linux OS\n- shell\n- at least python3.10\n\n### Installation\n\nFrom PyPi:\n\n```bash\n$ pip install --user pymum\n```\n\nOr you can install dirstory from the git repository:\n\n```bash\n$ pip install --user git+https://github.com/nikromen/mum\n```\n\n### Usage\n\nEnter the script\n\n```bash\n$ mum\n```\n\nThe script contain only a few commands and they are really simple. Here they are:\n\n`ls`\n\nOutput of this command:\n\n```\n┏━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┓\n┃ Monday ┃ Tuesday ┃ Wednesday  ┃ Thursday ┃ Friday ┃ Saturday   ┃ Sunday   ┃ Todo       ┃\n┡━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━┩\n│ cook   │ rave    │ cofee      │          │ drink  │ drink more │ hangover │ sleep      │\n│ eat    │ eat     │ more cofee │          │        │            │          │ sleep more │\n└────────┴─────────┴────────────┴──────────┴────────┴────────────┴──────────┴────────────┘\n```\n\n- will list all your work from the week in a table.\n- Subcommands:\n  - `ls [monday|tuesday|...|sunday|todo]`\n    - will list all your work from specific section. It can be days - `mum` saves the things you\'ve\n      done during the week in sections for each day, so you can view them individually.\n      You can also view the `todo` section\n\n`td [text]`\n\n- adds a text you specified into `todo` section\n- Subcommands:\n  - `td dn [int]`\n    - adds a corresponding `todo` item to a day section. You can view the number of `todo` item\n      via `ls todo` command.\n\n`dn [text]`\n\n- adds a text you specified to a corresponding day section\n\n`e section number_of_item [text]`\n\n- edits item of section\n- e.g.: `e monday 1 this is edited text` will edit first item in monday section to "this is edited\n  text"\n\n`mv section number_of_item section`\n\n- moves item from one section to another\n- e.g.: `mv friday 2 monday` will move second item from friday section to monday section\n\n`rst`\n\n- once you told your manager on standup/mtg/whatever what have you done, you can start new blank\n  session via `rst` command which will initialize new blank week.\n- Warning! The TODO section will not be removed! To remove even TODO section, use `rst all`\n\n`q`\n\n- quits `mum`\n',
    'author': 'Jiri Kyjovsky',
    'author_email': 'j1.kyjovsky@gmail.com',
    'maintainer': 'Jiří Kyjovský',
    'maintainer_email': 'j1.kyjovsky@gmail.com',
    'url': 'https://github.com/nikromen/mum',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
