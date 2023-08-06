from bittrade_kraken_rest.connection import send_public
from bittrade_kraken_rest.models.public.get_system_status import GetSystemStatusResult
from bittrade_kraken_rest.models.request import Response


def get_system_status() -> Response[GetSystemStatusResult]:
    return send_public(
        url='/0/public/SystemStatus',
        result_class=GetSystemStatusResult
    )