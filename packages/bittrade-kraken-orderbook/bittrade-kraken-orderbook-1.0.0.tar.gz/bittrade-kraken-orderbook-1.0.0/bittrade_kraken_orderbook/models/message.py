from typing import Union, NamedTuple, Any

class Message(NamedTuple):
    channel_id: int
    payload: Any
    channel_name: str
    pair: str


# Kraken has this strange message when updating both asks and bids where it comes with an extra payload bit instead
# of the payload containing both.

class TwoSideUpdateMessage(NamedTuple):
    channel_id: int
    payload_a: Any
    payload_b: Any
    channel_name: str
    pair: str


GenericMessage = Union[Message, TwoSideUpdateMessage]


def get_payload(raw_message):
    if is_two_side_update_message(raw_message):
        return dict(**raw_message[1], **raw_message[2])
    return raw_message[1]


def get_checksum(raw_message):
    return get_payload(raw_message).get('c')


def get_pair(raw_message):
    return raw_message[-1]

def is_two_side_update_message(message: GenericMessage) -> bool:
    return len(message) == 5
