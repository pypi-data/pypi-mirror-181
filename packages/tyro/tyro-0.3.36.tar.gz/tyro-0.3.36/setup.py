# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tyro', 'tyro.conf', 'tyro.extras']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'docstring-parser>=0.14.1,<0.15.0',
 'frozendict>=2.3.4,<3.0.0',
 'mypy>=0.991,<0.992',
 'rich>=11.1.0',
 'shtab>=1.5.6,<2.0.0',
 'typing-extensions>=4.3.0,<5.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['backports.cached-property>=1.0.2,<2.0.0'],
 ':sys_platform == "win32"': ['colorama>=0.4.0,<0.5.0']}

setup_kwargs = {
    'name': 'tyro',
    'version': '0.3.36',
    'description': 'Strongly typed, zero-effort CLI interfaces',
    'long_description': '<br />\n<p align="center">\n    <!--\n    Note that this README will be used for both GitHub and PyPI.\n    We therefore:\n    - Keep all image URLs absolute.\n    - In the GitHub action we use for publishing, strip some HTML tags that aren\'t supported by PyPI.\n    -->\n        <img alt="tyro logo" src="https://brentyi.github.io/tyro/_static/logo-light.svg" width="200px" />\n\n</p>\n\n<p align="center">\n    <em><a href="https://brentyi.github.io/tyro">Documentation</a></em>\n    &nbsp;&nbsp;&bull;&nbsp;&nbsp;\n    <em><code>pip install tyro</code></em>\n</p>\n\n<p align="center">\n    <img alt="build" src="https://github.com/brentyi/tyro/workflows/build/badge.svg" />\n    <img alt="mypy" src="https://github.com/brentyi/tyro/workflows/mypy/badge.svg?branch=main" />\n    <img alt="lint" src="https://github.com/brentyi/tyro/workflows/lint/badge.svg" />\n    <a href="https://codecov.io/gh/brentyi/tyro">\n        <img alt="codecov" src="https://codecov.io/gh/brentyi/tyro/branch/main/graph/badge.svg" />\n    </a>\n    <a href="https://pypi.org/project/tyro/">\n        <img alt="codecov" src="https://img.shields.io/pypi/pyversions/tyro" />\n    </a>\n</p>\n\n<br />\n\n<strong><code>tyro</code></strong> is a library for building CLI interfaces and\nconfiguration objects with type-annotated Python.\n\nOur core interface consists of one function, `tyro.cli()`, that generates\nargument parsers from Python callables and types.\n\n### A minimal example\n\nAs a replacement for `argparse`:\n\n<table align="">\n<tr>\n    <td><strong>with argparse</strong></td>\n    <td><strong>with tyro</strong></td>\n</tr>\n<tr>\n<td>\n\n```python\n"""Sum two numbers from argparse."""\n\nimport argparse\nparser = argparse.ArgumentParser()\nparser.add_argument(\n    "--a",\n    type=int,\n    required=True,\n)\nparser.add_argument(\n    "--b",\n    type=int,\n    default=3,\n)\nargs = parser.parse_args()\n\nprint(args.a + args.b)\n```\n\n</td>\n<td>\n\n```python\n"""Sum two numbers by calling a\nfunction with tyro."""\n\nimport tyro\n\ndef main(a: int, b: int = 3) -> None:\n    print(a + b)\n\ntyro.cli(main)\n```\n\n---\n\n```python\n"""Sum two numbers by instantiating\na dataclass with tyro."""\n\nfrom dataclasses import dataclass\n\nimport tyro\n\n@dataclass\nclass Args:\n    a: int\n    b: int = 3\n\nargs = tyro.cli(Args)\nprint(args.a + args.b)\n```\n\n</td>\n</tr>\n</table>\n\nFor more examples, see our [documentation](https://brentyi.github.io/tyro).\n\n### Why `tyro`?\n\n1. **Strong typing.**\n\n   Unlike tools dependent on dictionaries, YAML, or dynamic namespaces,\n   arguments populated by `tyro` benefit from IDE and language server-supported\n   operations — think tab completion, rename, jump-to-def, docstrings on hover —\n   as well as static checking tools like `pyright` and `mypy`.\n\n2. **Minimal overhead.**\n\n   Standard Python type annotations, docstrings, and default values are parsed\n   to automatically generate command-line interfaces with informative helptext.\n\n   `tyro` works seamlessly with tools you already use: examples are included for\n   [`dataclasses`](https://docs.python.org/3/library/dataclasses.html),\n   [`attrs`](https://www.attrs.org/),\n   [`pydantic`](https://pydantic-docs.helpmanual.io/),\n   [`flax.linen`](https://flax.readthedocs.io/en/latest/api_reference/flax.linen.html),\n   and more.\n\n   Hate `tyro`? Just remove one line of code, and you\'re left with beautiful,\n   type-annotated, and documented vanilla Python that can be used with a range\n   of other configuration libraries.\n\n3. **Modularity.**\n\n   `tyro` supports hierarchical configuration structures, which make it easy to\n   distribute definitions, defaults, and documentation of configurable fields\n   across modules or source files.\n\n4. **Tab completion.**\n\n   By extending [shtab](https://github.com/iterative/shtab), `tyro`\n   automatically generates tab completion scripts for bash, zsh, and tcsh.\n\n### In the wild\n\n`tyro` is still a new library, but being stress tested in several projects!\n\n- [nerfstudio-project/nerfstudio](https://github.com/nerfstudio-project/nerfstudio/)\n  provides a set of tools for end-to-end training, testing, and rendering of\n  neural radiance fields.\n- [Sea-Snell/JAXSeq](https://github.com/Sea-Snell/JAXSeq/) is a library for\n  distributed training of large language models in JAX.\n- [kevinzakka/obj2mjcf](https://github.com/kevinzakka/obj2mjcf) is an interface\n  for processing composite Wavefront OBJ files for Mujoco.\n- [brentyi/tensorf-jax](https://github.com/brentyi/tensorf-jax/) is an\n  unofficial implementation of\n  [Tensorial Radiance Fields](https://apchenstu.github.io/TensoRF/) in JAX.\n',
    'author': 'brentyi',
    'author_email': 'brentyi@berkeley.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/brentyi/tyro',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
