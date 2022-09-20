from telebox.dispatcher.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.enums.message_content_type import MessageContentType


class ContentTypeFilter(AbstractEventFilter):

    def __init__(self, *types: MessageContentType):
        self._types = set(types)

    def check_event(self, event: Message) -> bool:
        _, content_type = event.content

        return content_type in self._types
