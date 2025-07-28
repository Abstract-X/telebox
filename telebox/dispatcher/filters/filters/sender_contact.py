from typing import Optional

from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.types.message import Message
from telebox.bot.types.contact import Contact


class SenderContactFilter(AbstractFilter):

    def get_event_types(self) -> set[EventType]:
        return {EventType.MESSAGE, EventType.CHANNEL_POST}

    def get_value(self, event: Message) -> tuple[Optional[Contact], Optional[int]]:
        return event.contact, event.user_id

    def check_value(self, value: tuple[Optional[Contact], Optional[int]]) -> bool:
        contact, user_id = value

        return (contact is not None) and (contact.user_id == user_id)
