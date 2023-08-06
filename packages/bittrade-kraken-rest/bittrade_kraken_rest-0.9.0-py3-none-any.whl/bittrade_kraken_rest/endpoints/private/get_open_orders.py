import dataclasses

from bittrade_kraken_rest.connection import send_private
from bittrade_kraken_rest.environment.decorators import to_result
from bittrade_kraken_rest.models.private.get_open_orders import GetOpenOrdersOptions, GetOpenOrdersResponse, \
    GetOpenOrdersResult


def get_open_orders(*, options: GetOpenOrdersOptions = None):
    """
    Get open orders
    :param options: GetOpenOrdersOptions
    :return:
    """
    options = options or GetOpenOrdersOptions()
    return send_private(
        url='/0/private/OpenOrders',
        data=dataclasses.asdict(options),
    )
