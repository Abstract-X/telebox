from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.types.types.message import Message


class NewChatMemberIDFilter(AbstractEventFilter):

    def __init__(self, *ids: int):
        self._ids = set(ids)

    def get_event_types(self) -> set[EventType]:
        return {EventType.MESSAGE}

    def get_value(self, event: Message) -> set[int]:
        ids = set()

        if event.new_chat_members is not None:
            for i in event.new_chat_members:
                ids.add(i.id)

        return ids

    def check_value(self, value: set[int]) -> bool:
        return any(i in self._ids for i in value)
