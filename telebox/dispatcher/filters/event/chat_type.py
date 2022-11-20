from typing import Union

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message
from telebox.bot.types.types.callback_query import CallbackQuery
from telebox.bot.types.types.chat_member_updated import ChatMemberUpdated
from telebox.bot.types.types.chat_join_request import ChatJoinRequest


class ChatTypeFilter(AbstractEventFilter):

    def __init__(self, *types: str):
        if not types:
            raise ValueError("No chat types!")

        self._types = set(types)

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
    ) -> str:
        return event.chat_type

    def check_value(self, value: str) -> bool:
        return value in self._types
