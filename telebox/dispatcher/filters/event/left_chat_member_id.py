from typing import Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.types.types.message import Message


class LeftChatMemberIDFilter(AbstractEventFilter):

    def __init__(self, *ids: int):
        self._ids = set(ids)

    def get_event_types(self) -> set[EventType]:
        return {EventType.MESSAGE}

    def get_value(self, event: Message) -> Optional[int]:
        user = event.left_chat_member

        if user is not None:
            return user.id

    def check_value(self, value: Optional[int]) -> bool:
        return value in self._ids
