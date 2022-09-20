from telebox.dispatcher.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message


class SenderContactFilter(AbstractEventFilter):

    def check(self, event: Message) -> bool:
        return event.contact.user_id == event.from_.id
