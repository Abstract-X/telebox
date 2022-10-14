from telebox.dispatcher.filters.base_event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.enums.message_content_type import MessageContentType


class ContentTypeFilter(AbstractEventFilter):

    def __init__(self, *types: MessageContentType):
        self._types = set(types)

    def get_value(self, event: Message) -> MessageContentType:
        return event.content[1]

    def check_value(self, value: MessageContentType) -> bool:
        return value in self._types
