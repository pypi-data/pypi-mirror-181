# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lexer', 'lexer._tokenizer']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.6,<0.7']}

setup_kwargs = {
    'name': 'nr-io-lexer',
    'version': '1.0.0',
    'description': '',
    'long_description': '# nr.io.lexer\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
