from abc import abstractmethod
from typing import Optional, Any

from telebox.dispatcher.filters.filter import AbstractValueFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.typing import Event


class AbstractEventFilter(AbstractValueFilter):

    @abstractmethod
    def get_value(self, event: Event, event_type: EventType):
        pass

    def get_result(
        self,
        event: Event,
        event_type: EventType,
        values: Optional[dict[type, Any]] = None
    ) -> bool:
        values = values or {}

        try:
            value = values[type(self)]
        except KeyError:
            value = values[type(self)] = self.get_value(event, event_type)

        return self.check_value(value)
