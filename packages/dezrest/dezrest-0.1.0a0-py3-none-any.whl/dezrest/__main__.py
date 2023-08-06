r"""Serve ezbee via post port default 5555.

```bash
In: [str, str]
Out: List[Tuple[str, str, str]]

Tests:
curl -X 'POST' \
  'http://127.0.0.1:5555/post/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text1": "string",
  "text2": "string"
}'

res = httpx.post("http://127.0.0.1:5555/post/", json={'text1': 'a', 'text2': 'b'})
# res.json() = {'res': [['a', 'b', ''], ['c', 'c', '0.5']]}

x httpx.post("http://127.0.0.1:5555/post/", json=['a', 'b']).json()
httpx.post("http://127.0.0.1:5555/post/", json={'texts': ['a', 'b']}).json()

var r = await axios.post(`http://127.0.0.1:5555/post/`, { text1: 'a', text2: 'b' })
var r = await axios.post(`http://127.0.0.1:5555/post/`, { texts: ['a', 'b'] })
r.data
// { res: [ [ 'a', 'b', '' ], [ 'c', 'c', '0.5' ] ] }
```
"""
# pylint: disable=invalid-name, too-few-public-methods
# sanic sanic-app:app or sanic sanic-app.app
# http://127.0.0.1:8000
# from icecream import ic
# pylint: disable=invalid-name, no-name-in-module, unused-import
# import json
import os

# import signal
# from signal import SIG_DFL, SIGINT, signal
from typing import List, Tuple, Union

import logzero
import uvicorn

# from time import sleep
from ezbee import ezbee
from ezbee.gen_pairs import gen_pairs
from ezbee.save_xlsx_tsv_csv import save_xlsx_tsv_csv
from fastapi import FastAPI
from logzero import logger
from pydantic import BaseModel
from set_loglevel import set_loglevel

from dezrest import __version__

# import sys
# from argparse import Namespace  # from types import SimpleNamespace
# from pathlib import Path


# from sanic.log import logger

# from sanic import Sanic, response
# from sanic.response import text
# from sanic.exceptions import ServerError, NotFound


logzero.loglevel(set_loglevel())

# app = Sanic("MyHelloWorldApp")
debug = True
port = 5555

app = FastAPI(
    title="dezbee-rest",
    version=__version__,
    description=f"{__doc__}",
)


@app.get("/")
async def hello_world():
    """Trivial template."""
    # ic(request)
    # ic(request.args)
    # return text("Hello, world.")
    return {"greeting": "Hello from dezbee-rest"}


class Texts(BaseModel):
    """Define request body (not used)."""

    # text1: str
    # text2: str
    __root__: Tuple[str, str]


class ThreeCols(BaseModel):
    """Define response_model (not used)."""

    __root__: List[Tuple[str, str, Union[str, float]]]


# @app.post("/post/", response_model=ThreeCols)
# def on_post(texts: Texts):


@app.post("/post/", response_model=List[Tuple[str, str, str]])
def on_post(texts: Tuple[str, str]):
    """Deliver aligned pairs.

    ```
    Request body: [str, str]

    Response model: List[Tuple[str, str, str]]
    """
    # logger.debug(" d texts: %s", texts)

    text1, text2 = texts
    lists = text1.splitlines(), text2.splitlines()

    # list1, list2 = text1.splitlines(), text2.splitlines()
    # logger.debug("type(list1): %s, list1[:5]: %s", type(list1), list1[:5])
    # logger.debug("type(list2): %s, list2[:5]: %s", type(list2), list2[:5])

    # aset = ezbee(lines1, lines2)
    # aset = ezbee(list1, list2)

    aset = ezbee(*lists)

    logzero.loglevel(set_loglevel())
    if aset:
        logger.debug("aset: %s...%s", aset[:4], aset[-4:])
        # logger.debug("aset: %s", aset)

    # aligned_pairs = gen_pairs(list1, list2, aset)
    aligned_pairs = gen_pairs(*lists, aset)

    logger.debug("aligned_pairs[:5]: %s", aligned_pairs[:5])

    _ = """
    return [
        ['a', 'b', ''],
        ['c', 'd', .5],
    ]
    # """

    return aligned_pairs


if __name__ == "__main__":
    # sanic sanic-app:app -p 7777 --debug --workers=2
    # or python sanic-app.py  # production-mode
    #
    # app.run(host="0.0.0.0", port=8000, debug=True, auto_reload=True)  # dev=True
    # app.run(host="0.0.0.0", port=8000, auto_reload=True)
    # dev = True

    # app.run(port=port, auto_reload=True, workers=2, debug=debug)

    # uvicorn app:app --host 0.0.0.0 --port 5555
    # curl http://127.0.0.1:5555
    # curl -XPOST http://127.0.0.1:5555/post/ -H "accept: application/json"
    # -H "Content-Type: application/json" -d "{\"text1\": \"a b c\", \"text2\": \"d e f\"}"

    if set_loglevel() <= 10:
        reload = True
        workers = 1
    else:
        reload = False
        workers = 2

    logger.info(" pid: %s ", os.getcwd())

    uvicorn.run(
        "dezrest.__main__:app",
        # host='0.0.0.0',
        # host='127.0.0.1',
        port=port,
        # reload=True,
        workers=2,
        # debug=True,
        # timeout_keep_alive65,
        # log_level=10,
    )
