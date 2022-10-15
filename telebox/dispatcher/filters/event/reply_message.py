from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message


class ReplyMessageFilter(AbstractEventFilter):

    def get_value(self, event: Message) -> Message:
        return event

    def check_value(self, value: Message) -> bool:
        return value.is_reply
