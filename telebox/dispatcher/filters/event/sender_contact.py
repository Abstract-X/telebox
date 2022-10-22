from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message


class SenderContactFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.MESSAGE, EventType.CHANNEL_POST}

    def get_value(self, event: Message, event_type: EventType) -> bool:
        return (event.contact is not None) and (event.contact.user_id == event.user_id)

    def check_value(self, value: bool) -> bool:
        return value
