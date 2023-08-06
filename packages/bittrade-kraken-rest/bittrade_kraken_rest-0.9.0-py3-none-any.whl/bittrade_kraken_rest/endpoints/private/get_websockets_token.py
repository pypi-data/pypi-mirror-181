import dataclasses

from bittrade_kraken_rest.connection import send_private
from bittrade_kraken_rest.environment.decorators import to_result
from bittrade_kraken_rest.models.private.get_open_orders import GetOpenOrdersOptions, GetOpenOrdersResponse, \
    GetOpenOrdersResult
from bittrade_kraken_rest.models.private.get_websockets_token import GetWebsocketsTokenResult


def get_websockets_token():
    """
    Get websockets token
    :return:
    """
    return send_private(
        url='/0/private/GetWebSocketsToken', result_class=GetWebsocketsTokenResult
    )
