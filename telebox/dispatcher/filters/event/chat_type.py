from typing import Union, Optional

from telebox.dispatcher.filters.base_event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.types.types.callback_query import CallbackQuery
from telebox.telegram_bot.types.types.chat_member_updated import ChatMemberUpdated
from telebox.telegram_bot.types.types.chat_join_request import ChatJoinRequest


class ChatTypeFilter(AbstractEventFilter):

    def __init__(self, *types: str):
        self._types = set(types)

    def get_value(
        self,
        event: Union[
            Message,
            CallbackQuery,
            ChatMemberUpdated,
            ChatJoinRequest
        ]
    ) -> Optional[str]:
        return event.chat_type

    def check_value(self, value: Optional[str]) -> bool:
        return value in self._types
