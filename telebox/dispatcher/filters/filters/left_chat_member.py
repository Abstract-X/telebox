from typing import Optional

from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.types.message import Message


class LeftChatMemberFilter(AbstractFilter):

    def __init__(self, *user_ids: int):
        self._user_ids = set(user_ids)

    def get_event_types(self) -> set[EventType]:
        return {EventType.MESSAGE}

    def get_value(self, event: Message):
        return event.left_chat_member.id if event.left_chat_member is not None else None

    def check_value(self, value: Optional[int]) -> bool:
        if self._user_ids:
            return value in self._user_ids

        return value is not None
