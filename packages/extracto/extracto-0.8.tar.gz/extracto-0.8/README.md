# extracto

[![PyPI](https://img.shields.io/pypi/v/extracto.svg)](https://pypi.org/project/extracto/)
[![Changelog](https://img.shields.io/github/v/release/cldellow/extracto?include_prereleases&label=changelog)](https://github.com/cldellow/extracto/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/cldellow/extracto/blob/main/LICENSE)

Extract Python dicts from HTML files, fast.

Built on the very fast [selectolax](https://github.com/rushter/selectolax) library,
and applies a few tricks to make your life happier.

## Installation

Install this library using `pip`:

    pip install extracto

## Usage

```python
from extracto import prepare, extract_rows
from selectolax.parser import HTMLParser

html = '''
<h1>Famous Allens</h1>
<div data-occupation="actor">
  <div><b>Name</b> Alfie</div>
  <div><b>Year</b> 1986</div>
</div>
<div data-occupation="singer">
  <div><b>Name</b> Lily</div>
  <div><b>Year</b> 1985</div>
</div>
<div data-occupation="cocaine-trafficker">
  <div><b>Name</b> Tim</div>
  <div><b>Year</b> Unknown</div>
</div>
'''

tree = HTMLParser(html)

# Tweak the parsed DOM to be more amenable to scraping via CSS.
prepare(tree)

results = extract_rows(
    tree,
    {
        # Try to emit a row for every element matched by this selector
        'selector': 'h1 ~ div',
        'columns': [
            {
                # Columns are usually evaluated relative to the row selector,
                # but you can "break out" and have an absolute value by
                # prefixing the selector with "html"
                'selector': 'html h1'
                'conversions': [
                    # Strip "Famous" by capturing only the text that follows,
                    # and assigning it to the return value ('rv') group
                    re.compile('Famous (?P<rv>.+)')
                ]
            },
            {
                'selector': '.q-name + span',
            },
            {
                'selector': '.q-year + span',
                # Convert the year to an int
                'conversions': ['int'],
                # If we fail to extract something for this column, that's OK--just emit None
                'optional': True,
            },
            {
                'conversions': [
                  # Extract the value of the "data-occupation" attribute
                  '@data-occupation',
                  # Actors are boring
                  re.compile('singer|cocaine-trafficker'),
                ],
            }
        ]
    }
)
```

Will result in:

```
[
  [ 'Allens', 'Lily', 1985, 'singer' ],
  [ 'Allens', 'Tim', None, 'cocaine-trafficker' ],
]
```

Note that Alfie was excluded by the regular expression filter on
occupation, which permitted only `singer` and `cocaine-trafficker` rows
through.

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

    cd extracto
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
