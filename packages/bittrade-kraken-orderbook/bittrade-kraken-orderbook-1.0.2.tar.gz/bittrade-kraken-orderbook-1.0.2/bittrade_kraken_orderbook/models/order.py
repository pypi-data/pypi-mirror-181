from decimal import Decimal
import dataclasses
from typing import Union, List, Optional, Tuple

Order = Tuple[str, str, str]

RepublishOrder = Tuple[str, str, str, str]

GenericOrder = Union[Order, RepublishOrder]

def is_republish_order(order: GenericOrder) -> bool:
    return len(order) == 4


def get_volume(order: GenericOrder):
    return order[1]


def get_price(order: GenericOrder):
    return order[0]


def find_by_price(orders_list: List[GenericOrder], price: str) -> Optional[Order]:
    price = Decimal(price)
    for order in orders_list:
        order_price = Decimal(get_price(order))
        if price == order_price:
            return order
    return None


def find_insert_index_by_price(orders: List[GenericOrder], price: str, is_descending: bool) -> int:
    """
    Finds the index in the orders at which the price would be included.
    :param price:
    :param orders:
    :return: int Index at which to insert (or update) the order
    """
    price_decimal = Decimal(price)

    def is_order_before_price(o: GenericOrder):
        price = Decimal(get_price(order))
        if is_descending:
            return price > price_decimal
        return price < price_decimal

    for i, order in enumerate(orders):
        if not is_order_before_price(order):
            return i
    return len(orders)
