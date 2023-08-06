from bittrade_kraken_orderbook.models import Order
from bittrade_kraken_orderbook.models.order import get_price, get_volume


def clean(text: str):
    return text.replace('.', '').lstrip('0')
def stringify_single_entry(order: Order) -> str:
    price, volume = get_price(order), get_volume(order)
    return f'{clean(price)}{clean(volume)}'