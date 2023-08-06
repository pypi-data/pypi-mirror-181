# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yakh', 'yakh.key']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-yakh',
    'version': '0.3.0',
    'description': 'Yet Another Keypress Handler',
    'long_description': "# yakh\n\nyakh (Yet Another Keypress Handler) tries to handle keypresses from the stdin in the terminal in high-level platform indepdendent manner.\n\n## Usage\n\n```python\nfrom yakh import get_key\nfrom yakh.key import Keys\n\nkey = ''\nwhile key not in ['q', Keys.ENTER]:\n    key = get_key()\n    if key.is_printable:\n        print(key)\n```\n\nyakh is dead-simple, there is only one function `get_key()` which takes no arguments and blocks until a key is pressed.\n\nFor each keypress it creates an instance of [`Key`](./yakh/key/_key.py#L7) which holds:\n\n- `.key`: characters representing the keypress\n- `.key_codes`: collection of Unicode code point encodings for all the characters (given by `ord` function)\n- `.is_printable`: printability of the characters in the keypress\n\nAdditionally `Key` instances\n\n-  are comparable with another `Key` instances, `str` instances and *Unicode code point* representations (tuples of integers)\n- come with string representation for purposes of printing and string concatenation, which returns the content of `.key` attribute\n\n## `yakh.key` submodule\n`yakh.key` sub-module contains platform dependent representations of certain keys under `Keys` class. These are available namely for `CTRL` key combinations and some other common keys. \n\nFull list of keys can be seen [here](./yakh/key/_key.py#L42) and [here](./yakh/key/_key.py#L81).\n",
    'author': 'petereon',
    'author_email': 'pvyboch1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/petereon/yakh',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.8,<4.0.0',
}


setup(**setup_kwargs)
