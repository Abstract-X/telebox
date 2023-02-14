from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.dispatcher.enums.media_group_content_type import MediaGroupContentType


class MediaGroupContentTypeFilter(AbstractEventFilter):

    def __init__(self, *types: MediaGroupContentType):
        if not types:
            raise ValueError("No media group content types!")

        self._types = set(types)

    def get_event_types(self) -> set[EventType]:
        return {EventType.MEDIA_GROUP, EventType.CHANNEL_MEDIA_GROUP}

    def check_event(self, event: MediaGroup) -> bool:
        return all(i in self._types for i in event.content_types)
