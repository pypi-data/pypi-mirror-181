# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shrtcodes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'shrtcodes',
    'version': '1.0.1',
    'description': 'Simple shortcodes for Python.',
    'long_description': '# shrtcodes\n\n![example workflow name](https://github.com/Peter554/shrtcodes/workflows/CI/badge.svg)\n\n`pip install shrtcodes`\n\nSimple shortcodes for Python.\n\n## Example:\n\nA toy example:\n\n```\n# example.txt\nHello!\n\n{% img http://cutedogs.com/dog123.jpg "A very cute dog" %}\n\nFoo bar baz...\n\n{% repeat 3 %}\nWoop\n{% / %}\n\nBye!\n```\n\n```py\nfrom shrtcodes import Shrtcodes\n\n\nshortcodes = Shrtcodes()\n\n\n@shortcodes.register_inline("img")\ndef handle_img(src, alt):\n    return f\'<img src="{src}" alt="{alt}"/>\'\n\n\n@shortcodes.register_block("repeat")\ndef handle_repeat(block, n):\n    return block * int(n)\n\n\nwith open("example.txt") as f:\n    print(shortcodes.process_text(f.read()))\n```\n\nOutput:\n\n```\nHello!\n\n<img src="http://cutedogs.com/dog123.jpg" alt="A very cute dog"/>\n\nFoo bar baz...\n\nWoop\nWoop\nWoop\n\nBye!\n```\n\nA more useful example would be the generation of this README itself.\nSee [`/create_readme.py`](/create_readme.py) and [`/README.template.md`](/README.template.md).\n',
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
