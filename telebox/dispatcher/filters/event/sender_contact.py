from typing import Optional

from telebox.dispatcher.filters.base_event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message


class SenderContactFilter(AbstractEventFilter):

    def get_value(self, event: Message) -> tuple[Optional[int], Optional[int]]:
        if event.contact is not None:
            return event.contact.user_id, event.user_id

        return None, event.user_id

    def check_value(self, value: tuple[Optional[int], Optional[int]]) -> bool:
        contact_user_id, user_id = value

        return (contact_user_id is not None) and (contact_user_id == user_id)
