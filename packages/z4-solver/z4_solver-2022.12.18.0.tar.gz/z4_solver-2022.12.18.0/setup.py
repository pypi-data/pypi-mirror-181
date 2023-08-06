# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['z4']
install_requires = \
['z3-solver>=4.8,<5.0']

setup_kwargs = {
    'name': 'z4-solver',
    'version': '2022.12.18.0',
    'description': 'z3++',
    'long_description': '# z4\n\n[z3](https://github.com/Z3Prover/z3) with some improvements:\n* Change the right shift operation on `BitVec`\'s to be logical instead of arithmetic\n* Extend the `*` operation on `BoolRef`\'s to work between two `BoolRef`\'s.\n* Add additional operations to `BoolRef`\'s:\n  * `+`, returning an Int kind such that e.g `True+True+False==2`\n  * `&`, utilizing `And()`\n  * `|`, utilizing `Or()`\n  * `~`, utilizing `Not()`\n* Add the `ByteVec` class\n* Some helper methods for solving:\n  * `easy_solve`\n  * `find_all_solutions`\n  * `easy_prove`\n* Add some helper functions for z3 variables/constants:\n  * `BoolToInt`\n  * `Sgn`\n  * `Abs`\n  * `TruncDiv`\n\n## Usage\nInstall with `pip install z4-solver`.\n\nStandard usage:\n\n```python3\nimport z4\n\na, b = z4.Ints("a b")\nprint(*z4.find_all_solutions([a > 0, b > 0, a % b == 3, a > b, a + b == 19]), sep="\\n")\n```\n\nOutput:\n```\n[b = 4, a = 15, div0 = [else -> 3], mod0 = [else -> 3]]\n[b = 8, a = 11, div0 = [else -> 1], mod0 = [else -> 3]]\n```\n',
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
