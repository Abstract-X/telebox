from telebox.dispatcher.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message


class ForwardedMessageFilter(AbstractEventFilter):

    def check(self, event: Message) -> bool:
        return event.is_forwarded
