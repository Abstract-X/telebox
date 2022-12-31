from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.types.types.message import Message


class SenderContactFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.MESSAGE, EventType.CHANNEL_POST}

    def check_event(self, event: Message) -> bool:
        return (event.contact is not None) and (event.contact.user_id == event.user_id)
