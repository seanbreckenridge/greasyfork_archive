# Greasyfork User Archive

Scrape data from a users Greasyfork account.

For a given user, for each installable script that users created, scrapes:

```
script name
script authors
daily installs
total installs
rating score
created date
updated date
script type
script version
sensitive
language
css available as js
description
url
code (the script contents)
```

This does not scrape the script code for items that can't be installed directly, e.g. [this](https://greasyfork.org//en/scripts/36108-sortable-js/code)

##### Example

`greasyfork_archive 106222 --output-file scraped_data.json`

### Installation

To install with pip, run:

    pip3 install --user greasyfork_archive

### Run

```
Usage: greasyfork_archive [OPTIONS] GREASYFORK_USER_ID

Options:
  --output-file PATH  JSON filepath to output scraped data to  [required]
  --help              Show this message and exit.
```

### Tests

```
pip3 install --user pytest vcrpy
pytest
```
