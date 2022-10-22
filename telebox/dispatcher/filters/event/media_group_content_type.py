from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.media_group import MediaGroup
from telebox.dispatcher.enums.media_group_content_type import MediaGroupContentType


class MediaGroupContentTypeFilter(AbstractEventFilter):

    def __init__(self, *types: MediaGroupContentType):
        self._types = set(types)

    def get_value(self, event: Event, event_type: EventType) -> set[MediaGroupContentType]:
        if isinstance(event, MediaGroup):
            return event.content_types

    def check_value(self, value: set[MediaGroupContentType]) -> bool:
        return any(i in value for i in self._types) if self._types else bool(value)
