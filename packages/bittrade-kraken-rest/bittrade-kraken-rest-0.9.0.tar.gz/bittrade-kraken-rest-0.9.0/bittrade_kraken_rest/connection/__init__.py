from contextlib import contextmanager
import requests

from bittrade_kraken_rest.connection.nonce import get_nonce
from bittrade_kraken_rest.models.request import RequestWithResponse, Response

API_URL = 'https://api.kraken.com'


@contextmanager
def send_private(*, url: str, data=None, headers=None, result_class=None) -> RequestWithResponse:
    """

    :param url: Note that url is actually just the path here, starting with /0/private/...
    :param data:
    :param headers:
    :param result_class:
    :return:
    """
    data = data or {}
    headers = headers or {}
    if 'nonce' not in data:
        # we don't want to mutate `data` by adding the nonce
        data = dict(
            nonce=get_nonce(),
            **data
        )
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=utf-8'

    request = RequestWithResponse(
        method='POST',
        url=url,
        data=data,
        headers=headers
    )
    # Give context manager a chance to sign
    yield request
    request.url = f'{API_URL}{url}'
    request.response = Response(session.send(request.prepare()), result_class)


def send_public(*, url: str, params=None, headers=None, result_class=None
                ) -> Response:
    """Send request to Kraken public REST API.

    All public endpoints use GET

      Args:
          url (str): should start with a "/" or include the full kraken api domain (so you may use beta apis)
          params (dict): Query params
          headers:

      Returns:
          requests.Response:
    """
    headers = headers or {}
    params = params or {}

    headers['Content-Type'] = 'application/json'

    if not url.startswith(API_URL):
        url = f'{API_URL}{url}'

    return Response(session.get(url, params=params, headers=headers), result_class)


session = requests.Session()
