from typing import Union, Pattern, Optional

from telebox.dispatcher.filters.event.command import CommandFilter
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.utils import get_decoded_deep_link_payload


class StartCommandFilter(CommandFilter):

    def __init__(
        self,
        *,
        username: str,
        payload: Union[str, Pattern[str], None] = None,
        with_decoding: bool = False,
        ignore_case: bool = True
    ):
        super().__init__("/start", username=username, ignore_case=ignore_case)
        self._payload = payload
        self._with_decoding = with_decoding

    def get_value(self, event: Message) -> tuple[Optional[str], Optional[str]]:
        command = super().get_value(event)
        payload = None

        if (command is not None) and (self._payload is not None):
            try:
                payload = event.text.split(" ", 1)[1]
            except IndexError:
                pass
            else:
                if self._with_decoding:
                    payload = get_decoded_deep_link_payload(payload)

        return command, payload

    def check_value(self, value: tuple[Optional[str], Optional[str]]) -> bool:
        command, payload = value

        if super().check_value(command):
            if (self._payload is not None) and (payload is not None):
                if isinstance(self._payload, Pattern):
                    return self._payload.fullmatch(payload) is not None
                else:
                    return self._payload == payload

            return True

        return False
