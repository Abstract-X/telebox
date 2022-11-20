from typing import Optional, Union

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message
from telebox.bot.types.types.callback_query import CallbackQuery
from telebox.bot.types.types.chat_member_updated import ChatMemberUpdated
from telebox.bot.types.types.chat_join_request import ChatJoinRequest


class ChatIDFilter(AbstractEventFilter):

    def __init__(self, *ids: int):
        self._ids = set(ids)

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.CHANNEL_POST,
            EventType.EDITED_CHANNEL_POST,
            EventType.MEDIA_GROUP,
            EventType.CALLBACK_QUERY,
            EventType.MY_CHAT_MEMBER,
            EventType.CHAT_MEMBER,
            EventType.CHAT_JOIN_REQUEST
        }

    def get_value(
        self,
        event: Union[Message,
                     MediaGroup,
                     CallbackQuery,
                     ChatMemberUpdated,
                     ChatJoinRequest]
    ) -> Optional[int]:
        return event.chat_id

    def check_value(self, value: Optional[int]) -> bool:
        return value in self._ids if self._ids else value is not None
