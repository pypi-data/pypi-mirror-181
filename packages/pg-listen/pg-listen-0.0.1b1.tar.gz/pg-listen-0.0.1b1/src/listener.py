import logging
import select
from typing import Callable, NamedTuple, Dict

from .payload_types import PayloadType, PAYLOAD_DECODER

logger = logging.getLogger(__name__)


class ListenRules(NamedTuple):
    callback: Callable
    decoder: Callable


class Listener:
    _rules: Dict[str, ListenRules]

    def __init__(
            self,
            conn,
    ):
        self._rules = {}
        self.conn = conn

    def _register_listener(
            self,
            channel: str,
            callback: Callable,
            decoder: Callable,
    ):
        if channel in self._rules:
            raise Exception(f'Channel "{channel}" is already registered.')

        self._rules[channel] = ListenRules(callback, decoder)

    def _get_rule(self, channel):
        return self._rules.get(channel)

    def listen(
            self,
            channel: str,
            payload_type: PayloadType = PayloadType.STRING,
    ):
        def registrator(func):
            decoder = PAYLOAD_DECODER[payload_type]
            self._register_listener(
                channel=channel,
                callback=func,
                decoder=decoder,
            )
            return func

        return registrator

    def start(self):
        cursor = self.conn.cursor()
        for channel in self._rules:
            cursor.execute(f'LISTEN {channel};')
            logger.debug('Listening notifications from "%s"', channel)

        while True:
            select.select([self.conn], [], [])
            self.conn.poll()
            while self.conn.notifies:
                notify = self.conn.notifies.pop(0)
                # notify.pid, notify.channel, notify.payload
                rule = self._get_rule(notify.channel)
                if not rule:
                    continue

                try:
                    decoded_payload = rule.decoder(notify.payload)
                except Exception as e:
                    logger.error(e, exc_info=True)
                    continue

                rule.callback(decoded_payload or None)
