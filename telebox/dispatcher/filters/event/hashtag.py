from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.consts import message_entity_types


class HashtagFilter(AbstractEventFilter):

    def __init__(self, *hashtags: str, ignore_case: bool = True):
        self._hashtags = set()

        for i in hashtags:
            if not i.startswith("#"):
                i = f"#{i}"

            if ignore_case:
                i = i.lower()

            self._hashtags.add(i)

        self._ignore_case = ignore_case

    def get_value(self, event: Event, event_type: EventType) -> set[str]:
        hashtags = set()

        if isinstance(event, Message):
            for i in event.get_entities():
                if i.type == message_entity_types.HASHTAG:
                    hashtags.add(event.get_entity_text(i))

        return hashtags

    def check_value(self, value: set[str]) -> bool:
        if not self._hashtags:
            return bool(value)

        for i in value:
            if self._ignore_case:
                i = i.lower()

            if i in self._hashtags:
                return True

        return False
