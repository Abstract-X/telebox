from typing import Optional

from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.bot.types.message import Message
from telebox.bot.enums.message_type import MessageType


class MessageTypeFilter(AbstractFilter):
    def __init__(self, *types: MessageType):
        if not types:
            raise ValueError("No message types!")

        self._types = set(types)

    def get_value(self, event: Message) -> MessageType:
        return event.type

    def check_value(self, value: Optional[MessageType]) -> bool:
        return value in self._types
