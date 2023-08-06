import dataclasses
from typing import List, Any

from bittrade_kraken_orderbook.models.order import Order


@dataclasses.dataclass()
class OrderBook:
    asks: List[Order] = dataclasses.field(default_factory=list)  # not sticking with Kraken's naming because "as" is
    # a reserved keyword
    bids: List[Order] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class MetaOrderBook(OrderBook):
    timestamp: str = ''
    pair: str = ''


def is_snapshot_payload(payload: Any):
    return 'as' in payload
