from bittrade_kraken_orderbook.models import OrderBook
import zlib
from bittrade_kraken_orderbook.check.stringify import stringify_single_entry

def calculate_checksum(order_book: OrderBook) -> str:
    concatenated = ''
    for orders in (order_book.asks, order_book.bids):
        for order in orders[:10]:
            concatenated = f'{concatenated}{stringify_single_entry(order)}'
    return str(zlib.crc32(concatenated.encode()))