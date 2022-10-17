from typing import Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.types.types.callback_query import CallbackQuery
from telebox.telegram_bot.types.types.chat_member_updated import ChatMemberUpdated
from telebox.telegram_bot.types.types.chat_join_request import ChatJoinRequest


class ChatTypeFilter(AbstractEventFilter):

    def __init__(self, *types: str):
        if not types:
            raise ValueError("No chat types!")

        self._types = set(types)

    def get_value(self, event: Event, event_type: EventType) -> Optional[str]:
        if isinstance(event, (Message, CallbackQuery, ChatMemberUpdated, ChatJoinRequest)):
            return event.chat_type

    def check_value(self, value: Optional[str]) -> bool:
        return value in self._types
