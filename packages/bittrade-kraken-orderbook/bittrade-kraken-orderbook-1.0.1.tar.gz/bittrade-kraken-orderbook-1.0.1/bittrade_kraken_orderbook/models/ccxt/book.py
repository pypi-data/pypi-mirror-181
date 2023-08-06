import dataclasses
from typing import List

from bittrade_kraken_orderbook.models.ccxt.order import CcxtOrder


@dataclasses.dataclass
class CcxtOrderbook:
    asks: List[CcxtOrder]
    bids: List[CcxtOrder]