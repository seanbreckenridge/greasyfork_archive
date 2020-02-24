# Greasyfork User Archive

Scrape data from a users Greasyfork account

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
