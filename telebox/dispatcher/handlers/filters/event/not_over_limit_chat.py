from typing import Union

from telebox.dispatcher.handlers.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.types.types.callback_query import CallbackQuery


class NotOverLimitChatFilter(AbstractEventFilter):

    def __init__(self, over_limit_chat_ids: set[int]):
        self._over_limit_chat_ids = over_limit_chat_ids

    def get_value(
        self,
        event: Union[Message, CallbackQuery]
    ) -> int:
        return event.chat_id

    def check_value(self, value: int) -> bool:
        return value not in self._over_limit_chat_ids
