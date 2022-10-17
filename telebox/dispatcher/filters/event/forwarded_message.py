from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message
from telebox.typing import Event


class ForwardedMessageFilter(AbstractEventFilter):

    def get_value(self, event: Event, event_type: EventType) -> bool:
        return event.is_forwarded if isinstance(event, Message) else False

    def check_value(self, value: bool) -> bool:
        return value
