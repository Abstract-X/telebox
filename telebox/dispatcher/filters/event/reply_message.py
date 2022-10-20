from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message


class ReplyMessageFilter(AbstractEventFilter):

    def get_value(self, event: Event, event_type: EventType) -> bool:
        return event.is_reply if isinstance(event, Message) else False

    def check_value(self, value: bool) -> bool:
        return value
