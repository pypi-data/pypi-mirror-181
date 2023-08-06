# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textual_markdown']

package_data = \
{'': ['*']}

install_requires = \
['markdown-it-py[linkify,plugins]>=2.1.0,<3.0.0', 'textual[dev]>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'textual-markdown',
    'version': '0.1.0',
    'description': 'Markdown viewer widgets for Textual',
    'long_description': '# Textual Markdown Browser\n\nJust testing various Markdown content.\n\n[link](./demo.md)\n\n## Typography\n\n### Emphasis\n\nLets see if we can add text with *emphasis*. Typically rendered as italics.\n\n> Lets see if we can add text with *emphasis*. Typically rendered as italics. Lets see if we can add text with *emphasis*. Typically rendered as italics.\n> > Lets see if we can add text with *emphasis*. Typically rendered as italics.Lets see if we can add text with *emphasis*. Typically rendered as italics.\n\n### Strong\n\nWe can also render **strong** text as bold.\n\n### Strike\n\nWe can render ~~strikethrough~~ text.\n\n## Code\n\nRender a code "fence" with syntax highlighting.\n\n```python\n@lru_cache(maxsize=1024)\ndef split(self, cut_x: int, cut_y: int) -> tuple[Region, Region, Region, Region]:\n    """Split a region in to 4 from given x and y offsets (cuts).\n\n    ```\n                cut_x ↓\n            ┌────────┐ ┌───┐\n            │        │ │   │\n            │    0   │ │ 1 │\n            │        │ │   │\n    cut_y → └────────┘ └───┘\n            ┌────────┐ ┌───┐\n            │    2   │ │ 3 │\n            └────────┘ └───┘\n    ```\n\n    Args:\n        cut_x (int): Offset from self.x where the cut should be made. If negative, the cut\n            is taken from the right edge.\n        cut_y (int): Offset from self.y where the cut should be made. If negative, the cut\n            is taken from the lower edge.\n\n    Returns:\n        tuple[Region, Region, Region, Region]: Four new regions which add up to the original (self).\n    """\n\n    x, y, width, height = self\n    if cut_x < 0:\n        cut_x = width + cut_x\n    if cut_y < 0:\n        cut_y = height + cut_y\n\n    _Region = Region\n    return (\n        _Region(x, y, cut_x, cut_y),\n        _Region(x + cut_x, y, width - cut_x, cut_y),\n        _Region(x, y + cut_y, cut_x, height - cut_y),\n        _Region(x + cut_x, y + cut_y, width - cut_x, height - cut_y),\n    )\n```\n\n## Table\n\nGreat google moogly, its a GitHub style table in a TUI!\n\n| Name            | Type   | Default | Description                        |\n| --------------- | ------ | ------- | ---------------------------------- |\n| `show_header`   | `bool` | `True`  | Show the table header              |\n| `fixed_rows`    | `int`  | `0`     | Number of fixed rows               |\n| `fixed_columns` | `int`  | `0`     | Number of fixed columns            |\n| `zebra_stripes` | `bool` | `False` | Display alternating colors on rows |\n| `header_height` | `int`  | `1`     | Height of header row               |\n| `show_cursor`   | `bool` | `True`  | Show a cell cursor                 |\n\n\n## Bullet list\n\nA simple list of items.\n\n- This is a list\n- Another item\n  - Nested\n    - List items may have *formatting*    \n  - Yet another item\n\n## Ordered List\n\nOrder lists.\n\n1. Hello\n2. World\n   1. asdfsdf\n   2. werwer\n',
    'author': 'Will McGugan',
    'author_email': 'willmcgugan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
