# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dezrest']

package_data = \
{'': ['*']}

install_requires = \
['ezbee>=0.1.2,<0.2.0',
 'fastapi>=0.88.0,<0.89.0',
 'logzero>=1.7.0,<2.0.0',
 'pybind11>=2.10.1,<3.0.0',
 'sanic>=22.9.1,<23.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'set-loglevel>=0.1.2,<0.2.0',
 'uvicorn[standard]>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'dezrest',
    'version': '0.1.0a0',
    'description': 'serve ez/dz/de bee via FastAPI rest',
    'long_description': '# dezbee-rest\n[![pytest](https://github.com/ffreemt/dezbee-rest/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/dezbee-rest/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/dezrest.svg)](https://badge.fury.io/py/dezrest)\n\nServe [de|ez|dz]bee via FastAPI port 6666\n\n## python 3.8 only\n\n## Pre-install\n* fasttext\n  * `pip install fasttext` (linux) or `pip install fasttext*whl` (Windows)\n* pycld2, PyICU\n  * e.g. `poetry run pip install pycld2-0.41-cp38-cp38-win_amd64.wh PyICU-2.9-cp38-cp38-win_amd64.whl` \n* polyglot fix:\n  * `poetry run pip install -U git+https://github.com/aboSamoor/polyglot.git@master` or\n  *  `pip install artifects\\polyglot-16.7.4.tar.gz` (modified cloned polyglot: futures removed from requirements.txt)\n* scikit-learn (for deprecated sklearn used in some packages) and pybind11 (for Windows)\n\nRefer to [workflows](https://github.com/ffreemt/dezbee-rest/blob/main/.github/workflows/routine-tests.yml)\n\n## Install it\n\n##\n```shell\npip install dezrest\n# pip install git+https://github.com/ffreemt/dezbee-rest\n# poetry add git+https://github.com/ffreemt/dezbee-rest\n# git clone https://github.com/ffreemt/dezbee-rest && cd dezbee-rest\n```\n\n## Use it\n\n```bash\n# sart the server at port 5555 via `uvicorn` with 2 workers\npython -m dezrest\n\n# docs\nhttp://127.0.0.1:5555/docs\n```\n',
    'author': 'ffreemt',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ffreemt/dezbee-rest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
