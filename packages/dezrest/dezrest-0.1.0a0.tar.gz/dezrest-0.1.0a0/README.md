# dezbee-rest
[![pytest](https://github.com/ffreemt/dezbee-rest/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/dezbee-rest/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/dezrest.svg)](https://badge.fury.io/py/dezrest)

Serve [de|ez|dz]bee via FastAPI port 6666

## python 3.8 only

## Pre-install
* fasttext
  * `pip install fasttext` (linux) or `pip install fasttext*whl` (Windows)
* pycld2, PyICU
  * e.g. `poetry run pip install pycld2-0.41-cp38-cp38-win_amd64.wh PyICU-2.9-cp38-cp38-win_amd64.whl` 
* polyglot fix:
  * `poetry run pip install -U git+https://github.com/aboSamoor/polyglot.git@master` or
  *  `pip install artifects\polyglot-16.7.4.tar.gz` (modified cloned polyglot: futures removed from requirements.txt)
* scikit-learn (for deprecated sklearn used in some packages) and pybind11 (for Windows)

Refer to [workflows](https://github.com/ffreemt/dezbee-rest/blob/main/.github/workflows/routine-tests.yml)

## Install it

##
```shell
pip install dezrest
# pip install git+https://github.com/ffreemt/dezbee-rest
# poetry add git+https://github.com/ffreemt/dezbee-rest
# git clone https://github.com/ffreemt/dezbee-rest && cd dezbee-rest
```

## Use it

```bash
# sart the server at port 5555 via `uvicorn` with 2 workers
python -m dezrest

# docs
http://127.0.0.1:5555/docs
```
