# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdirpy']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['mkdirpy = mkdirpy:run']}

setup_kwargs = {
    'name': 'mkdirpy',
    'version': '0.1.1',
    'description': 'Like `mkdir`, but with `__init__.py` inside',
    'long_description': '# mkdirpy\n\nLike `mkdir` but with `__init__.py` inside\n\n## Installation\n\n```\npip install mkdirpy\n```\n\n## Usage\n\nThe syntax is identical to `mkdir`:\n\n```\nmkdirpy foo\n```\n\nWill create `foo` directory and `foo/__init__.py`\n\nUse `-p` flag to generate parent directories recursively:\n\n```\nmkdirpy -p foo/bar\n```\n\nWill create `foo`, `foo/__init__.py`, `foo/bar`, `foo/bar/__init__.py`\n\nAdd `-v` flag for verbose output:\n\n```\nmkdirpy -pv foo/bar\n```\n\nOutput:\n\n```\nfoo\nfoo/__init__.py\nfoo/bar\nfoo/bar/__init__.py\n```\n',
    'author': 'Olzhas Arystanov',
    'author_email': 'o.arystanov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/olzhasar/mkdirpy',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
