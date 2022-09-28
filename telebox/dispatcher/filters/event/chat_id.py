from typing import Union

from telebox.dispatcher.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.types.types.callback_query import CallbackQuery
from telebox.telegram_bot.types.types.chat_member_updated import ChatMemberUpdated
from telebox.telegram_bot.types.types.chat_join_request import ChatJoinRequest


class ChatIDFilter(AbstractEventFilter):

    def __init__(self, *ids: int):
        self._ids = set(ids)

    def check(
        self,
        event: Union[
            Message,
            CallbackQuery,
            ChatMemberUpdated,
            ChatJoinRequest
        ]
    ) -> bool:
        return event.chat_id in self._ids
