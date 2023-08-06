import requests

from bittrade_kraken_rest.connection import send_public
from bittrade_kraken_rest.models.public.get_server_time import GetServerTimeResult
from bittrade_kraken_rest.models.request import Response


def get_server_time() -> Response[GetServerTimeResult]:
    return send_public(
        url='/0/public/Time',
        result_class=GetServerTimeResult
    )
