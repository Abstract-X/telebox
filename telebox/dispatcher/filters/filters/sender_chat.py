from typing import Union, Optional

from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message


class SenderChatFilter(AbstractFilter):

    def __init__(self, *ids: int):
        self._ids = set(ids)

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.CHANNEL_POST,
            EventType.EDITED_CHANNEL_POST,
            EventType.MEDIA_GROUP,
            EventType.CHANNEL_MEDIA_GROUP
        }

    def get_value(self, event: Union[Message, MediaGroup]) -> Optional[int]:
        return event.sender_chat_id

    def check_value(self, value: Optional[int]) -> bool:
        if self._ids:
            return value in self._ids

        return value is not None
