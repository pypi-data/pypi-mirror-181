# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['z4']
install_requires = \
['z3-solver>=4.8,<5.0']

setup_kwargs = {
    'name': 'z4-solver',
    'version': '2022.12.18.1',
    'description': 'z3++',
    'long_description': '# z4\n\n[![PyPI](https://img.shields.io/pypi/v/z4-solver)](https://pypi.org/project/z4-solver/)\n\n[z3](https://github.com/Z3Prover/z3) with some improvements:\n* Change the right shift operation on `BitVec`\'s to be logical instead of arithmetic\n* Extend the `*` operation on `BoolRef`\'s to work between two `BoolRef`\'s.\n* Add additional operations to `BoolRef`\'s:\n  * `+`, returning an Int kind such that e.g `True + True + False == 2`\n  * `&`, utilizing `And()`\n  * `|`, utilizing `Or()`\n  * `~`, utilizing `Not()`\n* Add the `ByteVec` class\n* Some helper methods for solving:\n  * `easy_solve`\n  * `find_all_solutions`\n  * `easy_prove`\n* Add some helper functions for z3 variables/constants:\n  * `BoolToInt`\n  * `Sgn`\n  * `Abs`\n  * `TruncDiv`\n\n## Usage\nInstall with `pip install z4-solver`.\n\n### `easy_solve`\n```python3\nimport z4\n\na, b = z4.Ints("a b")\nprint(z4.easy_solve([a <= 10, b <= 10, a + b == 15]))\n```\n\nOutput:\n```\n[b = 5, a = 10]\n```\n\n### `find_all_solutions`\n```python3\nimport z4\n\na, b = z4.Ints("a b")\nprint(*z4.find_all_solutions([a <= 10, b <= 10, a + b == 15]), sep="\\n")\n```\n\nOutput:\n```\n[b = 5, a = 10]\n[b = 6, a = 9]\n[b = 7, a = 8]\n[b = 8, a = 7]\n[b = 9, a = 6]\n[b = 10, a = 5]\n```\n\n### `easy_prove`\nLet\'s try and prove that `2 * a >= a` for all integers `a`:\n```python3\nimport z4\n\na = z4.Int("a")\nprint(z4.easy_prove(2 * a >= a))\n```\n\nOutput\n```\nTraceback (most recent call last):\n  ...\nz4.Z3CounterExample: [a = -1]\n```\n\nThis isn\'t true so we get an exception with the counter-example `a = -1`. Of course `2 * -1 = -2` which is less than `-1`.\n\nLet\'s try again with the assumption that `a` must be non-negative:\n```python3\nprint(z4.easy_prove(z4.Implies(a >= 0, 2 * a >= a)))\n```\n\nOutput:\n```\nTrue\n```\n',
    'author': 'Asger Hautop Drewsen',
    'author_email': 'asgerdrewsen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Tyilo/z4',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
