# CharStripper
![PyPI - Downloads](https://img.shields.io/pypi/dm/charstripper) ![PyPI - License](https://img.shields.io/pypi/l/charstripper) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/charstripper) ![PyPI](https://img.shields.io/pypi/v/charstripper) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/charstripper) ![PyPI - Implementation](https://img.shields.io/pypi/implementation/charstripper)

This program replaces multiple characters in a text and also optionally lowers it.

## Installation
```
pip install charstripper
```

## Usage
You can import this script and use it like this:
```
from CharStripper.core import CharStripper

cs = CharStripper({'o': 'e', 'r': 't', ' ': ''}, True)
cs.strip('Bo aR L  OS')  # returns 'beatles'
```

`CharStripper` class takes one mandatory and one optional input.
- `charsDict` Gets a dictionary which replaces the dictionary keys with the dictionary values.
- `isLowercase` Is a boolean which returns the value lowercased.

After defining the class, you can call `cs.strip('YOUR_TEXT_HERE')` for every repetition.
