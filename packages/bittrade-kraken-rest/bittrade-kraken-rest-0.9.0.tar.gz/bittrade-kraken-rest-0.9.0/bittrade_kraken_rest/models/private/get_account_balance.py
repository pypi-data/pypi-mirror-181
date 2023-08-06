from typing import Dict

from ..message import KrakenMessage
import dataclasses

GetAccountBalanceResult = Dict[str, str]


@dataclasses.dataclass
class GetAccountBalanceResponse(KrakenMessage):
    result: GetAccountBalanceResult
