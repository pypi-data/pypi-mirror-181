from bittrade_kraken_orderbook.models import Order

def clean(text: str):
    return text.replace('.', '').lstrip('0')
def stringify_single_entry(order: Order) -> str:
    price, volume = order.price, order.volume
    return f'{clean(price)}{clean(volume)}'