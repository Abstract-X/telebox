from typing import Optional

from telebox.dispatcher.filter import AbstractFilter
from telebox.bot.types.message import Message


class LeftChatMemberFilter(AbstractFilter):
    def __init__(self, *user_ids: int):
        self._user_ids = set(user_ids)

    def get_value(self, event: Message) -> Optional[int]:
        if event.left_chat_member is not None:
            return event.left_chat_member.id

    def check_value(self, value: Optional[int]) -> bool:
        if self._user_ids:
            return value in self._user_ids

        return value is not None
