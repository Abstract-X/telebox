from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.dispatcher.enums.media_group_content_type import MediaGroupContentType


class MediaGroupContentTypeFilter(AbstractEventFilter):

    def __init__(self, *types: MediaGroupContentType):
        if not types:
            raise ValueError("No media group content types!")

        self._types = set(types)

    def get_event_types(self) -> set[EventType]:
        return {EventType.MEDIA_GROUP}

    def get_value(self, event: MediaGroup) -> set[MediaGroupContentType]:
        return event.content_types

    def check_value(self, value: set[MediaGroupContentType]) -> bool:
        return any(i in value for i in self._types)
