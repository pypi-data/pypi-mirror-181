import dataclasses
from typing import List, Dict, Optional, Literal

from ..message import KrakenMessage
from ..order import Order


@dataclasses.dataclass
class GetWebsocketsTokenResult:
    expires: int
    token: str


@dataclasses.dataclass
class GetOpenOrdersResponse(KrakenMessage):
    result: GetWebsocketsTokenResult


@dataclasses.dataclass
class GetOpenOrdersOptions:
    trades: bool = False
    userref: Optional[int] = None
    start: Optional[int] = None
    end: Optional[int] = None
    ofs: Optional[int] = None
    closetime: Optional[Literal["open", "close", "both"]] = "both"
