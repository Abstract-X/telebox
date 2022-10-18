from typing import Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message


class HashtagFilter(AbstractEventFilter):

    def __init__(self, *hashtags: str, ignore_case: bool = True):
        if not hashtags:
            raise ValueError("No hashtags!")

        self._hashtags = set()

        for i in hashtags:
            if not i.startswith("#"):
                i = f"#{i}"

            if ignore_case:
                i = i.lower()

            self._hashtags.add(i)

        self._ignore_case = ignore_case

    def get_value(self, event: Event, event_type: EventType) -> Optional[str]:
        if isinstance(event, Message) and (event.text is not None):
            hashtag = event.text.split(" ", 1)[0]

            return hashtag.lower() if self._ignore_case else hashtag

    def check_value(self, value: Optional[str]) -> bool:
        return value in self._hashtags
