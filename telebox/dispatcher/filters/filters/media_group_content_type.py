from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.types.media_group import MediaGroup
from telebox.dispatcher.enums.media_group_content_type import MediaGroupContentType


class MediaGroupContentTypeFilter(AbstractFilter):
    def __init__(self, *types: MediaGroupContentType):
        if not types:
            raise ValueError("No media group content types!")

        self._types = set(types)

    def get_value(self, event: MediaGroup) -> set[MediaGroupContentType]:
        return event.content_types

    def check_value(self, value: set[MediaGroupContentType]) -> bool:
        return all(i in self._types for i in value)
