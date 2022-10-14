from typing import Union, Pattern, Optional

from telebox.dispatcher.filters.event.command import CommandFilter
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

    def check_value(self, value: Optional[str]) -> bool:
        if super().check_value(value):
            if self._payload is not None:
                text_parts = value.split(" ", 1)

                if len(text_parts) == 2:
                    payload = text_parts[1]

                    if self._with_decoding:
                        payload = get_decoded_deep_link_payload(payload)

                    if isinstance(self._payload, Pattern):
                        return self._payload.fullmatch(payload) is not None
                    else:
                        return self._payload == payload
            else:
                return True

        return False
