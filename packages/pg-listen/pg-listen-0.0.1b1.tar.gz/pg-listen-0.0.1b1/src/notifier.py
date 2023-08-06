from typing import Union

from .payload_types import PAYLOAD_ENCODER


class Notifier:
    def __init__(
            self,
            conn,
    ):
        self.cursor = conn.cursor()

    def notify(
            self,
            channel: str,
            payload: Union[str, int, dict],
    ):
        encoder = PAYLOAD_ENCODER[type(payload)]
        encoded_payload = encoder(payload)
        self.cursor.execute(f"NOTIFY {channel}, '{encoded_payload}';")
