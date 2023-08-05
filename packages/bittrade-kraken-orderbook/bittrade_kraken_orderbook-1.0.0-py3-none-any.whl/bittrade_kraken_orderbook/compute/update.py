from decimal import Decimal
from typing import Literal, List, Dict, Optional

from bittrade_kraken_orderbook.models import OrderBook
from bittrade_kraken_orderbook.models.order import GenericOrder, Order, find_by_price, get_volume, get_price, \
    find_insert_index_by_price

from logging import getLogger

LOGGER = getLogger(__name__)


def update_side(side: Literal['bids', 'asks'], order_book: OrderBook, updated_orders: List[List[str]]):
    current_orders: List[Order] = getattr(order_book, side)
    order: List[str]
    is_descending = side == 'bids'
    book_length = len(current_orders)
    for order in updated_orders:
        volume = Decimal(get_volume(order))
        price = get_price(order)
        if volume == 0:
            # Removing order
            matching_order = find_by_price(current_orders, price)
            if not matching_order:
                LOGGER.error('Expected to find an order with price %s but did not. Orders: %s', price, current_orders)
            else:
                current_orders.remove(matching_order)
        else:
            # Matching order may not exist
            order_index = find_insert_index_by_price(current_orders, price, is_descending=is_descending)
            new_order = Order(*order[:3])
            # Could be an exact match
            try:
                order_at_index = current_orders[order_index]
                if Decimal(order_at_index.price) == Decimal(price):
                    # That's an update
                    current_orders[order_index] = new_order
                else:
                    # insert
                    current_orders.insert(order_index, new_order)
            except IndexError as exc:
                # means we are appending .... this happens when one order is removed and thus another one appended
                current_orders.append(new_order)
    # Skim the book to same length as before
    setattr(order_book, side, current_orders[:book_length])




def update_bids(order_book: OrderBook, payload: Dict):
    update_side('bids', order_book, payload['b'])


def update_asks(order_book: OrderBook, payload: Dict):
    update_side('asks', order_book, payload['a'])