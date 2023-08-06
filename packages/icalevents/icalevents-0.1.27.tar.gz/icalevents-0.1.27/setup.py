# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['icalevents']

package_data = \
{'': ['*']}

install_requires = \
['DateTime>=4.3,<5.0',
 'httplib2>=0.20.4,<0.21.0',
 'icalendar==4.0.9',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2021.3,<2022.0']

setup_kwargs = {
    'name': 'icalevents',
    'version': '0.1.27',
    'description': 'Simple Python 3 library to download, parse and query iCal sources.',
    'long_description': '# iCalEvents\n\nSimple Python 3 library to download, parse and query iCal sources.\n\n[![PyPI version](https://badge.fury.io/py/icalevnt.svg)](https://badge.fury.io/py/icalevnt)[![Jazzband](https://jazzband.co/static/img/badge.svg)](https://jazzband.co/)\n\n## Build info\n\nlast push: ![run pytest](https://github.com/jazzband/icalevents/actions/workflows/python-test.yml/badge.svg)\n\nmaster: [![Run pytest](https://github.com/jazzband/icalevents/actions/workflows/python-test.yml/badge.svg?branch=master)](https://github.com/jazzband/icalevents/actions/workflows/python-test.yml)\n\n## Documentation\n\nhttps://icalevents.readthedocs.io/en/latest/\n\n## Usage\n\n### iCloud:\n\n```python\n\nfrom icalevents.icalevents import events\n\nes  = events(<iCloud URL>, fix_apple=True)\n```\n\n### Google:\n\n```python\n\nfrom icalevents.icalevents import events\n\nes  = events(<Google Calendar URL>)\n```\n\n# Contributing\n\nYou will need [poetry](https://github.com/python-poetry/poetry) and [pre-commit](https://pre-commit.com/index.html) installed and than run.\n\n```bash\npre-commit install\n```\n\nHappy contributing!\n',
    'author': 'Martin Eigenmann',
    'author_email': 'github@eigenmannmartin.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
