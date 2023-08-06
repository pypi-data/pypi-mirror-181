# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shrtcodes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'shrtcodes',
    'version': '1.0.4',
    'description': 'Simple shortcodes for Python.',
    'long_description': '# shrtcodes\n\n![example workflow name](https://github.com/Peter554/shrtcodes/workflows/CI/badge.svg)\n\n`pip install shrtcodes`\n\nShortcodes for Python.\n\n## Example:\n\nA toy example.\n\nDefine our shortcodes:\n\n```py\n# example.py\nfrom shrtcodes import Shrtcodes\n\n\nshortcodes = Shrtcodes()\n\n\n# {% img src alt %} will create an image.\n@shortcodes.register_inline("img")\ndef handle_img(src, alt):\n    return f\'<img src="{src}" alt="{alt}"/>\'\n\n\n# {% repeat n %}...{% / %} will repeat a block n times.\n@shortcodes.register_block("repeat")\ndef handle_repeat(block, n):\n    return block * int(n)\n\n\n# we can call process_text to get the final text.\nin_text = "..."\nout_text = shortcodes.process_text(in_text)\n\n# or, we can create a CLI.\nshortcodes.create_cli()\n\n```\n\n```\npython example.py --help\n```\n\n```\nusage: example.py [-h] [--check_file CHECK_FILE] in_file\n\npositional arguments:\n  in_file               File to be processed\n\noptions:\n  -h, --help            show this help message and exit\n  --check_file CHECK_FILE\n                        Checks the output against this file and errors if\n                        there is a diff\n\n```\n\nWrite some text:\n\n```\n# example.txt\nHello!\n\n{% img http://cutedogs.com/dog123.jpg "A very cute dog" %}\n\nFoo bar baz...\n\n{% repeat 3 %}\nWoop\n{% / %}\n\nBye!\n```\n\nProcess the text:\n\n```\npython example.py example.txt\n```\n\n```\nHello!\n\n<img src="http://cutedogs.com/dog123.jpg" alt="A very cute dog"/>\n\nFoo bar baz...\n\nWoop\nWoop\nWoop\n\nBye!\n```\n\nA more useful example would be the generation of this README itself.\nSee [`create_readme.py`](/create_readme.py) and [`README.template.md`](/README.template.md).\n',
    'author': 'Peter Byfield',
    'author_email': 'byfield554@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Peter554/shrtcodes#readme',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
