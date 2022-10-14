from telebox.dispatcher.filters.base_event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message


class ForwardedMessageFilter(AbstractEventFilter):

    def get_value(self, event: Message) -> Message:
        return event

    def check_value(self, value: Message) -> bool:
        return value.is_forwarded
