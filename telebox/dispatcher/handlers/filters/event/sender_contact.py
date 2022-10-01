from telebox.dispatcher.handlers.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message


class SenderContactFilter(AbstractEventFilter):

    def get_value(self, event: Message) -> tuple[int, int]:
        return event.contact.user_id, event.from_.id

    def check_value(self, value: tuple[int, int]) -> bool:
        contact_user_id, user_id = value

        return contact_user_id == user_id
