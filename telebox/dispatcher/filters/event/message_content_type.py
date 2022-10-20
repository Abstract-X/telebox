from typing import Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.enums.message_content_type import MessageContentType


class MessageContentTypeFilter(AbstractEventFilter):

    def __init__(self, *types: MessageContentType):
        self._types = set(types)

    def get_value(self, event: Event, event_type: EventType) -> Optional[MessageContentType]:
        if isinstance(event, Message):
            _, content_type = event.content

            return content_type

    def check_value(self, value: Optional[MessageContentType]) -> bool:
        return value in self._types if self._types else bool(value)
