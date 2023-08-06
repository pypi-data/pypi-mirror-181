# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pathlib_tree']

package_data = \
{'': ['*']}

install_requires = \
['cli-toolkit>=2.2,<3.0', 'filemagic>=1.6,<2.0', 'pylint>=2.14,<3.0']

extras_require = \
{':sys_platform == "win32"': ['python-magic-bin>=0.4.14,<0.5.0']}

setup_kwargs = {
    'name': 'pathlib-tree',
    'version': '2.4.0',
    'description': 'Filesystem tree utilities',
    'long_description': '![Unit Tests](https://github.com/hile/pathlib-tree/actions/workflows/unittest.yml/badge.svg)\n![Style Checks](https://github.com/hile/pathlib-tree/actions/workflows/lint.yml/badge.svg)\n\n# Tree extension for pathlib.Path\n\nThis module implements an extensible tree-like object `pathlib_tree.Tree` that can be iterated\nand subclassed to use for various filesystem tree processing tasks.\n',
    'author': 'Ilkka Tuohela',
    'author_email': 'hile@iki.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
