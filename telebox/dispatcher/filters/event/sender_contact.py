from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message


class SenderContactFilter(AbstractEventFilter):

    def get_value(self, event: Event, event_type: EventType) -> bool:
        return (
            isinstance(event, Message)
            and (event.contact is not None)
            and (event.contact.user_id == event.user_id)
        )

    def check_value(self, value: bool) -> bool:
        return value
