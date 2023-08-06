from decimal import Decimal
from typing import NamedTuple, Union, List, Optional


class Order(NamedTuple):
    price: str
    volume: str
    timestamp: str


class RepublishOrder(NamedTuple):
    price: str
    volume: str
    timestamp: str
    republish = "r"


GenericOrder = Union[Order, RepublishOrder]

RawOrder = List[str]


def is_republish_order(order: GenericOrder) -> bool:
    return len(order) == 4


def get_volume(order: RawOrder):
    return order[1]


def get_price(order: RawOrder):
    return order[0]


def find_by_price(orders_list: List[GenericOrder], price: str) -> Optional[Order]:
    for order in orders_list:
        order_price = Decimal(order.price)
        price = Decimal(price)
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
        if is_descending:
            return Decimal(o.price) > price_decimal
        return Decimal(o.price) < price_decimal

    for i, order in enumerate(orders):
        if not is_order_before_price(order):
            return i
    return len(orders)
