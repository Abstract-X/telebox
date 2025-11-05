from __future__ import annotations
from typing import TYPE_CHECKING

from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.enums.event_type import EventType
if TYPE_CHECKING:
    from telebox.dispatcher.type_hints import Event


class NoneFilter(AbstractFilter):

    def get_event_types(self) -> set[EventType]:
        return set(EventType)

    def get_value(self, event: Event) -> bool:
        return True

    def check_value(self, value: bool) -> bool:
        return value
