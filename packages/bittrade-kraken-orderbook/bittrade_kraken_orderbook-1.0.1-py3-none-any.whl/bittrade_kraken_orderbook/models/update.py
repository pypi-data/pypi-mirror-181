import dataclasses
from typing import List, Any

from bittrade_kraken_orderbook.models.order import GenericOrder


@dataclasses.dataclass
class AsksUpdate:
    a: List[GenericOrder]
    c: str


@dataclasses.dataclass
class BidsUpdate:
    b: List[GenericOrder]
    c: str

def is_bids_update_payload(payload: Any):
    return 'b' in payload


def is_asks_update_payload(payload: Any):
    return 'a' in payload
