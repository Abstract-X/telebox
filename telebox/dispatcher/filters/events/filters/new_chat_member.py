from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.types.types.message import Message


class NewChatMemberFilter(AbstractEventFilter):

    def __init__(self, *user_ids: int):
        self._user_ids = set(user_ids)

    def get_event_types(self) -> set[EventType]:
        return {EventType.MESSAGE}

    def check_event(self, event: Message) -> bool:
        if event.new_chat_members:
            if not self._user_ids:
                return True

            for i in event.new_chat_members:
                if i in self._user_ids:
                    return True

        return False
