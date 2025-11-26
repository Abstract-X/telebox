from typing import Union, Optional

from telebox.dispatcher.filter import AbstractFilter
from telebox.dispatcher.types.media_group import MediaGroup
from telebox.bot.types.message import Message


class SenderChatFilter(AbstractFilter):
    def __init__(self, *ids: int):
        self._ids = set(ids)

    def get_value(self, event: Union[Message, MediaGroup]) -> Optional[int]:
        return event.sender_chat_id

    def check_value(self, value: Optional[int]) -> bool:
        if self._ids:
            return value in self._ids

        return value is not None
