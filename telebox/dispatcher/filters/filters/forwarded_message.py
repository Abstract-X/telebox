from typing import Union

from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.types.media_group import MediaGroup
from telebox.bot.types.message import Message


class ForwardedMessageFilter(AbstractFilter):
    def get_value(self, event: Union[Message, MediaGroup]) -> bool:
        return event.is_forwarded

    def check_value(self, value: bool) -> bool:
        return value
