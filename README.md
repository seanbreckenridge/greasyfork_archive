# Greasyfork User Archive

[![PyPi version](https://img.shields.io/pypi/v/greasyfork_archive.svg)](https://pypi.org/project/greasyfork-archive) 
[![Python 3.6|3.7|3.8|3.9](https://img.shields.io/pypi/pyversions/greasyfork_archive.svg)](https://pypi.org/project/greasyfork-archive)
[![Build Status](https://travis-ci.com/seanbreckenridge/greasyfork_archive.svg?branch=master)](https://travis-ci.com/seanbreckenridge/greasyfork_archive)
[![PRs
Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)


Scrape data from a users Greasyfork account.

For a given user, for each installable script that users created, scrapes:

```
script id
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

This does not scrape the script code for items that can't be installed directly, e.g. [this](https://greasyfork.org//en/scripts/36108-sortable-js/code).

##### Example

`greasyfork_archive 106222 --output-file scraped_data.json`

This would scrape information for the user https://greasyfork.org/en/users/106222

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
