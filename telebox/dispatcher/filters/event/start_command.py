from typing import Optional

from telebox.dispatcher.filters.event.command import CommandFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.utils import get_decoded_deep_link_payload


class StartCommandFilter(CommandFilter):

    def __init__(
        self,
        *payloads: str,
        username: str,
        with_decoding: bool = False,
        ignore_case: bool = True
    ):
        super().__init__("/start", username=username, ignore_case=ignore_case)
        self._payloads = set(payloads)
        self._with_decoding = with_decoding

    def get_value(
        self,
        event: Event,
        event_type: EventType
    ) -> tuple[Optional[str], Optional[str]]:
        command = super().get_value(event, event_type)

        if (command is not None) and self._payloads:
            payload = get_payload(event.text, with_decoding=self._with_decoding)
        else:
            payload = None

        return command, payload

    def check_value(self, value: tuple[Optional[str], Optional[str]]) -> bool:
        command, payload = value

        if super().check_value(command):
            if self._payloads:
                return payload in self._payloads

            return True

        return False


def get_payload(text: str, *, with_decoding: bool) -> Optional[str]:
    try:
        payload = text.split(" ", 1)[1]
    except IndexError:
        payload = None
    else:
        if with_decoding:
            payload = get_decoded_deep_link_payload(payload)

    return payload
