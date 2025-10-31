from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.types.message import Message
from telebox.bot.enums.message_type import MessageType


class MessageTypeFilter(AbstractFilter):

    def __init__(self, *types: MessageType):
        if not types:
            raise ValueError("No message types!")

        self._types = set(types)

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.CHANNEL_POST,
            EventType.EDITED_CHANNEL_POST
        }

    def get_value(self, event: Message) -> MessageType:
        return event.type

    def check_value(self, value: MessageType) -> bool:
        return value in self._types
