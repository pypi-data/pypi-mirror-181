# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shrtcodes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'shrtcodes',
    'version': '1.0.0',
    'description': 'Simple shortcodes for Python.',
    'long_description': '# shrtcodes\n\n![example workflow name](https://github.com/Peter554/shrtcodes/workflows/CI/badge.svg)\n\n`pip install shrtcodes`\n\nSimple shortcodes for Python.\n\n## Example:\n\n```py\nfrom shrtcodes import Shrtcodes\n\nin_text = """\nHello!\n\n{% img http://cutedogs.com/dog123.jpg "A very cute dog" %}\n\nFoo bar baz...\n\n{% repeat 3 %}\nWoop\n{% / %}\n\nBye!\n""".strip()\n\nshortcodes = Shrtcodes()\n\n\n@shortcodes.register_inline("img")\ndef handle_img(src, alt):\n    return f\'<img src="{src}" alt="{alt}"/>\'\n\n\n@shortcodes.register_block("repeat")\ndef handle_repeat(block, n):\n    return block * int(n)\n\n\nout_text = shortcodes.process_text(in_text)\nprint(out_text)\n\n```\n\nOutput:\n\n```\nHello!\n\n<img src="http://cutedogs.com/dog123.jpg" alt="A very cute dog"/>\n\nFoo bar baz...\n\nWoop\nWoop\nWoop\n\nBye!\n\n```',
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
