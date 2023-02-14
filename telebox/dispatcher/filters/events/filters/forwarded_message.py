from typing import Union

from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message


class ForwardedMessageFilter(AbstractEventFilter):

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.CHANNEL_POST,
            EventType.MEDIA_GROUP,
            EventType.CHANNEL_MEDIA_GROUP
        }

    def check_event(self, event: Union[Message, MediaGroup]) -> bool:
        return event.is_forwarded
