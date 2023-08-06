import dataclasses
from typing import Literal

from ..message import KrakenMessage

Status = Literal["online", "maintenance", "cancel_only", "post_only"]


@dataclasses.dataclass
class GetSystemStatusResult:
    status: Status
    timestamp: str


@dataclasses.dataclass
class GetSystemStatusResponse(KrakenMessage):
    result = GetSystemStatusResult
