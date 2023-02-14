from typing import Union

from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message


class ReplyMessageFilter(AbstractEventFilter):

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

    def check_event(self, event: Union[Message, MediaGroup]) -> bool:
        if event.is_reply:
            if self._user_ids:
                return event.reply_to_message.user_id in self._user_ids

            return True

        return False
