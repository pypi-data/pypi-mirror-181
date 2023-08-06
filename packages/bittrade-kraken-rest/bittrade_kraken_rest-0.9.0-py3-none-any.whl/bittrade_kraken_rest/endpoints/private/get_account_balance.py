from bittrade_kraken_rest.connection import send_private
from bittrade_kraken_rest.models.private.get_account_balance import GetAccountBalanceResult


def get_account_balance():
    """
    Get account balances
    :return:
    """
    return send_private(
        url='/0/private/Balance',
    )
