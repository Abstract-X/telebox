from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.bot.types.message import Message
from telebox.bot.types.user import User


class NewChatMemberFilter(AbstractFilter):
    def __init__(self, *user_ids: int):
        self._user_ids = set(user_ids)

    def get_value(self, event: Message) -> list[User]:
        return event.new_chat_members or []

    def check_value(self, value: list[User]) -> bool:
        if value:
            if not self._user_ids:
                return True

            for i in value:
                if i.id in self._user_ids:
                    return True

        return False
