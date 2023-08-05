from typing import List

from bittrade_kraken_orderbook.compute.snapshot import load_snapshot
from bittrade_kraken_orderbook.compute.update import update_bids, update_asks
from bittrade_kraken_orderbook.models import (
    Message,
    TwoSideUpdateMessage,
    Order, RepublishOrder, OrderBook
)
from threading import Lock
from bittrade_kraken_orderbook.models.message import GenericMessage, is_two_side_update_message, get_payload
from bittrade_kraken_orderbook.models.orderbook import is_snapshot_payload
from bittrade_kraken_orderbook.models.update import is_bids_update_payload, is_asks_update_payload

lock = Lock()


def compute_order_book(order_book: OrderBook, message: List) -> None:
    """
    Computes the change effected by the message and mutates the orderbook accordingly.
    This does not perform the CRC32 check which needs to be done elsewhere
    :param order_book:
    :param message:
    :return:
    """
    payload = get_payload(message)
    with lock:
        if is_snapshot_payload(payload):
            load_snapshot(order_book, payload)
            return
        # do not return within `if` since message can actually be both sides
        if is_bids_update_payload(payload):
            update_bids(order_book, payload)
        if is_asks_update_payload(payload):
            update_asks(order_book, payload)




