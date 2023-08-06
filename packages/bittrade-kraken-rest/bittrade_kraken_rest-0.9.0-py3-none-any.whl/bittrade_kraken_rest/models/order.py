import dataclasses
from typing import Dict, List


@dataclasses.dataclass
class Order:
    refid: str
    userref: str
    status: str
    opentm: int
    starttm: int
    expiretm: int
    descr: Dict
    vol: str
    vol_exec: str
    cost: str
    fee: str
    price: str
    stopprice: str
    limitprice: str
    trigger: str
    misc: str
    oflags: str
    trades: List