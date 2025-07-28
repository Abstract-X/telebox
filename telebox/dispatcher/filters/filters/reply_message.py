from typing import Union, Optional

from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.message import Message


class ReplyMessageFilter(AbstractFilter):

    def __init__(self, *user_ids: int):
        self._user_ids = set(user_ids)

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.CHANNEL_POST,
            EventType.EDITED_CHANNEL_POST,
            EventType.MEDIA_GROUP,
            EventType.CHANNEL_MEDIA_GROUP
        }

    def get_value(self, event: Union[Message, MediaGroup]) -> Optional[Message]:
        return event.reply_to_message

    def check_value(self, value: Optional[Message]) -> bool:
        if value is not None:
            if self._user_ids:
                return value.user_id in self._user_ids

            return True

        return False
