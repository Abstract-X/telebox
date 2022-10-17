from typing import Pattern, Optional

from telebox.dispatcher.filters.event.command import CommandFilter
from telebox.dispatcher.filters.event.start_command import get_payload
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType


class RegExpStartCommandFilter(CommandFilter):

    def __init__(
        self,
        *payloads: Pattern,
        username: str,
        with_decoding: bool = False,
        ignore_case: bool = True
    ):
        super().__init__("/start", username=username, ignore_case=ignore_case)
        self._payloads = payloads
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
            if self._payloads and (payload is not None):
                return any(i.fullmatch(payload) is not None for i in self._payloads)

            return True

        return False
