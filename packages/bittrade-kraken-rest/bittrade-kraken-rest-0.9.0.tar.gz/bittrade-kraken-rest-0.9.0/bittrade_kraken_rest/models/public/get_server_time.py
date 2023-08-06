from bittrade_kraken_rest.models.message import KrakenMessage
import dataclasses


@dataclasses.dataclass
class GetServerTimeResult:
    unixtime: int
    rfc1123: str


@dataclasses.dataclass
class GetServerTimeResponse(KrakenMessage):
    result: GetServerTimeResult
