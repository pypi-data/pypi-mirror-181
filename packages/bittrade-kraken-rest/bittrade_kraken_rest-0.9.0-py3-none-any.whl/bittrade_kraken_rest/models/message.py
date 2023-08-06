import dataclasses
from typing import List, Union, Dict


@dataclasses.dataclass
class KrakenMessage:
    error: List[str]
    result: Union[List, Dict]