import dataclasses
from functools import wraps
from os import getenv
import requests
from typing import Any, Callable, List

from bittrade_kraken_rest.exceptions.error import KrakenError


def with_api_key(func):
    @wraps(func)
    def fn(api_key: str = '', **kwargs):
        if not api_key:
            api_key = getenv('KRAKEN_API_KEY')
        if not api_key:
            raise ValueError('API key needs to be passed to methods or set as environment variable KRAKEN_API_KEY')
        return func(api_key=api_key, **kwargs)

    return fn


def to_result(dataclass: dataclasses.dataclass, func: Callable[[Any], requests.Response]):
    def fn(**kwargs):
        response = func(**kwargs)
        if not response.ok:
            response.raise_for_status()
        body = response.json()
        if body['error']:
            raise KrakenError(','.join(body['error']))
        return dataclass(**body['result'])
    return fn
