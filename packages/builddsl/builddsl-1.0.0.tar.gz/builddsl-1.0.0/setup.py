# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['builddsl']

package_data = \
{'': ['*']}

install_requires = \
['nr-io-lexer>=1.0.0,<2.0.0', 'typing-extensions>=3.0.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.6,<0.7']}

setup_kwargs = {
    'name': 'builddsl',
    'version': '1.0.0',
    'description': 'A superset of the Python programming language with support for closures and multi-line lambdas.',
    'long_description': '# builddsl\n\nA superset of the Python programming language with support for closures and multi-line lambdas.\n\nBuildDSL is an "almost superset" of Python 3; adding a lot of syntactical features that make it more\nconvenient to describe build configurations at the cost of some other syntax features of the native Python\nlanguage (like set literals).\n\n## Installation\n\n    $ pip install builddsl\n\nThe `builddsl` package requires at least Python 3.8.\n\n## Projects using BuildDSL\n\n* [Novella](https://niklasrosenstein.github.io/novella/)\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
