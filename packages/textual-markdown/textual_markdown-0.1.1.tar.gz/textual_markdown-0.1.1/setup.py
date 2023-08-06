# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textual_markdown']

package_data = \
{'': ['*']}

install_requires = \
['markdown-it-py[linkify,plugins]>=2.1.0,<3.0.0', 'textual[dev]>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'textual-markdown',
    'version': '0.1.1',
    'description': 'Markdown viewer widgets for Textual',
    'long_description': '# Textual Markdown Browser\n\nThis project is an experiment to see how far I could take the idea of a "Markdown browser" in the terminal, using the [Textual](https://github.com/Textualize/textual) framework.\n\nMarkdown in the terminal is not unusual, [Rich](https://github.com/Textualize/rich) has a decent Markdown renderer, but its output is essentially static. Textual Markdown creates a more dynamic Markdown document you can interact with: there are working links, srollablr code fences, and tables.\n\nLinks must be relative only and on the filesystem for now. These could be made to load from the network for a more browser like experience. It is also relatively easy to intercept links and handle them programatically. Opening up custom hypertext like applications.\n\nAnd finally, there is a TOC (Table Of Contents) extracted from the Markdown, which can be used to navigate the document.\n\n## Video\n\nA short video of me playing with the demo Markdown.\n\nhttps://user-images.githubusercontent.com/554369/208234316-be4e6626-c601-4dca-b8d1-59af9b4d08cd.mov\n\n\n## Screenshots\n\n![Screenshot 2022-12-17 at 08 41 58](https://user-images.githubusercontent.com/554369/208233944-542b1fec-daaf-4c4b-81d1-2d9eec61e727.png)\n\n\n![Screenshot 2022-12-17 at 08 42 33](https://user-images.githubusercontent.com/554369/208233987-9667dd87-5ef3-45c3-91fc-166f069e14cb.png)\n\n![Screenshot 2022-12-17 at 08 42 38](https://user-images.githubusercontent.com/554369/208233988-f0733761-6794-41f9-893f-f0258b23b988.png)\n\n## Try it out\n\nYou can install `textual-markdown` from PyPI in the usual way:\n\n```\npip install textual-markdown\n```\n\nHere\'s how you hopen a Markdown file:\n\n```\npython -m textual_markdown README.md\n```\n\n## Disclaimer\n\nAt time of writing, there is less than a weeks work in this. Which means you may (likely) find bugs. \n\n## The future\n\nSome (or all) of this repo will be rolled in to [Textual](https://github.com/Textualize/textual). It may also become a project in its own right. If there is enough interest.\n',
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
