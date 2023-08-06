# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poltergeist']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poltergeist',
    'version': '0.3.1',
    'description': 'Experimental Rust-like error handling in Python, with type-safety in mind.',
    'long_description': '# poltergeist\n\n[![pypi](https://img.shields.io/pypi/v/poltergeist.svg)](https://pypi.python.org/pypi/poltergeist)\n[![versions](https://img.shields.io/pypi/pyversions/poltergeist.svg)](https://github.com/alexandermalyga/poltergeist)\n\nExperimental Rust-like error handling in Python, with type-safety in mind.\n\n## Installation\n\n```\npip install poltergeist\n```\n\n## Examples\n\nUse the provided `@poltergeist` decorator on any function:\n\n```python\nfrom pathlib import Path\nfrom poltergeist import Err, Ok, poltergeist\n\n@poltergeist(OSError)\ndef read_text(path: Path) -> str:\n    return path.read_text()\n\n# Result of type Result[str, OSError]\nresult = read_text(Path("test.txt"))\n\n# Get the contained Ok value or raise the contained Err exception\ncontent = result.unwrap()\n\n# Get the contained Ok value or a provided default\ncontent = result.unwrap_or("default text")\n\n# Get the contained Ok value or compute it from a callable\ncontent = result.unwrap_or_else(lambda e: f"The exception was: {e}")\n\n# Get the contained Err exception or None\nerr = result.err()\n\n# Handle errors using structural pattern matching\nmatch result:\n    case Ok(content):\n        # Type-checkers know the return type of the original function\n        print("File content in upper case:", content.upper())\n    case Err(e):\n        match e:\n            # The exception type is also known\n            case FileNotFoundError():\n                print("File not found:", e.filename)\n            case PermissionError():\n                print("Permission error:", e.errno)\n            case _:\n                raise e\n```\n\nYou can also wrap errors yourself:\n\n```python\nfrom pathlib import Path\nfrom poltergeist import Err, Ok, Result\n\ndef read_text(path: Path) -> Result[str, FileNotFoundError]:\n    try:\n        return Ok(path.read_text())\n    except FileNotFoundError as e:\n        return Err(e)\n```\n\nBoth of these examples pass type checking and provide in-editor autocompletion.\n',
    'author': 'Alexander Malyga',
    'author_email': 'alexander@malyga.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alexandermalyga/poltergeist',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
