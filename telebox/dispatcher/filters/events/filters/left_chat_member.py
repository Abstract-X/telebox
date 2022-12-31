from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.types.types.message import Message


class LeftChatMemberFilter(AbstractEventFilter):

    def __init__(self, *user_ids: int):
        self._user_ids = set(user_ids)

    def get_event_types(self) -> set[EventType]:
        return {EventType.MESSAGE}

    def check_event(self, event: Message) -> bool:
        user_id = event.left_chat_member.id if event.left_chat_member is not None else None

        if self._user_ids:
            return user_id in self._user_ids

        return user_id is not None
