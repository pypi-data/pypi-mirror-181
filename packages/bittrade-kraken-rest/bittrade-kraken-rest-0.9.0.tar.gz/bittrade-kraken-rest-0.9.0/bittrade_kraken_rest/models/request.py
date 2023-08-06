import dataclasses
import json
from contextlib import contextmanager
from typing import TypeVar, Generic, List

import requests

T = TypeVar("T")


class Response(Generic[T]):
    as_json = None

    def __init__(self, response: requests.Response, result_class: T):
        self.response = response
        self._result_class = result_class
        try:
            self.as_json = response.json()
        except json.JSONDecodeError:
            pass

    def get_result(self) -> T:
        return self._result_class(**self.as_json['result'])

    def get_error(self) -> List[str]:
        return self.as_json['error']

    @property
    def request(self):
        return self.response.request


class RequestWithResponse(Generic[T], requests.Request):
    response: Response[T]
