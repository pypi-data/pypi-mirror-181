# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['squiral']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['squiral = squiral.main:main_cli']}

setup_kwargs = {
    'name': 'squiral',
    'version': '0.3.0',
    'description': 'squiral - square spiral',
    'long_description': '# squiral\n[![](https://img.shields.io/pypi/v/squiral)](https://pypi.org/project/squiral/)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n[![](https://img.shields.io/pypi/pyversions/squiral.svg)](https://pypi.org/project/squiral/)\n[![Downloads](https://pepy.tech/badge/squiral)](https://pepy.tech/project/squiral)\n<br/>\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sadikkuzu/squiral/main.svg)](https://results.pre-commit.ci/latest/github/sadikkuzu/squiral/main)\n[![Python lint&test](https://github.com/sadikkuzu/squiral/actions/workflows/python-package.yml/badge.svg)](https://github.com/sadikkuzu/squiral/actions/workflows/python-package.yml)\n[![Publish Python Package](https://github.com/sadikkuzu/squiral/actions/workflows/python-publish.yml/badge.svg)](https://github.com/sadikkuzu/squiral/actions/workflows/python-publish.yml)\n\n**squ**are sp**iral**\n\n```\nWelcome to Squiral!\nHere is an example:\n21 22 23 24 25\n20  7  8  9 10\n19  6  1  2 11\n18  5  4  3 12\n17 16 15 14 13\n```\n\nThe basic idea behind printing this matrix is<br/>\nto start from the middle of the matrix and then moving:<br/>\n`right` >> `down` >> `left` >> `up`<br/>\nand not returning to the same row again.\n\n### Install\n\n#### [PyPI](https://pypi.org/project/squiral/)\n\n```shell\npip install squiral\n```\n\n#### [GitHub](https://github.com/sadikkuzu/squiral)\n\n```shell\npip install git+https://github.com/sadikkuzu/squiral.git\n```\n\n### Usage\n\n#### In console:\n\n```console\nbuddha@dharma:~$ squiral 7\n43 44 45 46 47 48 49\n42 21 22 23 24 25 26\n41 20  7  8  9 10 27\n40 19  6  1  2 11 28\n39 18  5  4  3 12 29\n38 17 16 15 14 13 30\n37 36 35 34 33 32 31\nbuddha@dharma:~$ squiral --help\nusage: squiral [-h] size\n\npositional arguments:\n  size        squiral size\n\noptional arguments:\n  -h, --help  show this help message and exit\n```\n\n#### In python:\n\n```python\n>>> import squiral as sq\n>>> sq.printout(sq.produce(5))\n21 22 23 24 25\n20  7  8  9 10\n19  6  1  2 11\n18  5  4  3 12\n17 16 15 14 13\n>>>\n```\n',
    'author': 'SADIK KUZU',
    'author_email': 'sadikkuzu@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sadikkuzu/squiral',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
