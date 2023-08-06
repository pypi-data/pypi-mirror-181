## mum

A simple tool to help you keep track of your work throughout the week, it also helps you
keep track of short-term todo stuff. It will remind you during the week so you don't
have to think about it. Just like mums do to little kids :)

## Table of contents

<!-- toc -->

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

<!-- tocstop -->

### Requirements

- linux OS
- shell
- at least python3.10

### Installation

From PyPi:

```bash
$ pip install --user pymum
```

Or you can install dirstory from the git repository:

```bash
$ pip install --user git+https://github.com/nikromen/mum
```

### Usage

Enter the script

```bash
$ mum
```

The script contain only a few commands and they are really simple. Here they are:

`ls`

Output of this command:

```
┏━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Monday ┃ Tuesday ┃ Wednesday  ┃ Thursday ┃ Friday ┃ Saturday   ┃ Sunday   ┃ Todo       ┃
┡━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━┩
│ cook   │ rave    │ cofee      │          │ drink  │ drink more │ hangover │ sleep      │
│ eat    │ eat     │ more cofee │          │        │            │          │ sleep more │
└────────┴─────────┴────────────┴──────────┴────────┴────────────┴──────────┴────────────┘
```

- will list all your work from the week in a table.
- Subcommands:
  - `ls [monday|tuesday|...|sunday|todo]`
    - will list all your work from specific section. It can be days - `mum` saves the things you've
      done during the week in sections for each day, so you can view them individually.
      You can also view the `todo` section

`td [text]`

- adds a text you specified into `todo` section
- Subcommands:
  - `td dn [int]`
    - adds a corresponding `todo` item to a day section. You can view the number of `todo` item
      via `ls todo` command.

`dn [text]`

- adds a text you specified to a corresponding day section

`e section number_of_item [text]`

- edits item of section
- e.g.: `e monday 1 this is edited text` will edit first item in monday section to "this is edited
  text"

`mv section number_of_item section`

- moves item from one section to another
- e.g.: `mv friday 2 monday` will move second item from friday section to monday section

`rst`

- once you told your manager on standup/mtg/whatever what have you done, you can start new blank
  session via `rst` command which will initialize new blank week.
- Warning! The TODO section will not be removed! To remove even TODO section, use `rst all`

`q`

- quits `mum`
