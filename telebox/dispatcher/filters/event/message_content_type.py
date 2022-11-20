from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.types.types.message import Message
from telebox.bot.enums.message_content_type import MessageContentType


class MessageContentTypeFilter(AbstractEventFilter):

    def __init__(self, *types: MessageContentType):
        if not types:
            raise ValueError("No message content types!")

        self._types = set(types)

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.CHANNEL_POST,
            EventType.EDITED_CHANNEL_POST
        }

    def get_value(self, event: Message) -> MessageContentType:
        _, content_type = event.content

        return content_type

    def check_value(self, value: MessageContentType) -> bool:
        return value in self._types
