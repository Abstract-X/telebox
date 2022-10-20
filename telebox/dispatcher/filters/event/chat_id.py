from typing import Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.types.types.callback_query import CallbackQuery
from telebox.telegram_bot.types.types.chat_member_updated import ChatMemberUpdated
from telebox.telegram_bot.types.types.chat_join_request import ChatJoinRequest


class ChatIDFilter(AbstractEventFilter):

    def __init__(self, *ids: int):
        self._ids = set(ids)

    def get_value(self, event: Event, event_type: EventType) -> Optional[int]:
        if isinstance(event, (Message, CallbackQuery, ChatMemberUpdated, ChatJoinRequest)):
            return event.chat_id

    def check_value(self, value: Optional[int]) -> bool:
        return value in self._ids if self._ids else value is not None
