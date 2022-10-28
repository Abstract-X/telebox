from abc import ABC, abstractmethod
from typing import Optional, Any

from telebox.dispatcher.enums.event_type import EventType


class AbstractEventBaseFilter(ABC):

    def __invert__(self):
        return InvertEventFilter(self)

    def __and__(self, other):
        if isinstance(other, ConjunctionEventFilter):
            return ConjunctionEventFilter(self, *other)
        elif isinstance(other, AbstractEventBaseFilter):
            return ConjunctionEventFilter(self, other)

        return NotImplemented

    def __or__(self, other):
        if isinstance(other, DisjunctionEventFilter):
            return DisjunctionEventFilter(self, *other)
        elif isinstance(other, AbstractEventBaseFilter):
            return DisjunctionEventFilter(self, other)

        return NotImplemented

    @abstractmethod
    def get_event_types(self) -> set[EventType]:
        pass

    @abstractmethod
    def check_event_type(self, event_type: EventType) -> bool:
        pass

    @abstractmethod
    def get_result(self, event, values: Optional[dict[type, Any]] = None) -> bool:
        pass


class AbstractEventFilter(AbstractEventBaseFilter, ABC):

    def check_event_type(self, event_type: EventType) -> bool:
        return event_type in self.get_event_types()

    @abstractmethod
    def get_value(self, event):
        pass

    @abstractmethod
    def check_value(self, value) -> bool:
        pass

    def get_result(self, event, values: Optional[dict[type, Any]] = None) -> bool:
        values = values or {}

        try:
            value = values[type(self)]
        except KeyError:
            value = values[type(self)] = self.get_value(event)

        return self.check_value(value)


class InvertEventFilter(AbstractEventBaseFilter):

    def __init__(self, filter_: AbstractEventBaseFilter):
        self.filter = filter_

    def __repr__(self):
        return f"{type(self).__name__}({self.filter!r})"

    def __invert__(self):
        return self.filter

    def get_event_types(self) -> set[EventType]:
        return self.filter.get_event_types()

    def check_event_type(self, event_type: EventType) -> bool:
        return event_type in self.filter.get_event_types()

    def get_result(self, event, values: Optional[dict[type, Any]] = None) -> bool:
        return not self.filter.get_result(event, values)


class ConjunctionEventFilter(AbstractEventBaseFilter):

    def __init__(self, *filters: AbstractEventBaseFilter):
        self.filters = filters

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(repr(i) for i in self.filters)})"

    def __iter__(self):
        return iter(self.filters)

    def __and__(self, other):
        if isinstance(other, ConjunctionEventFilter):
            return ConjunctionEventFilter(*self, *other)
        elif isinstance(other, AbstractEventBaseFilter):
            return ConjunctionEventFilter(*self, other)

        return NotImplemented

    def get_event_types(self) -> set[EventType]:
        types = set()

        for i in self.filters:
            types.update(i.get_event_types())

        return types

    def check_event_type(self, event_type: EventType) -> bool:
        for i in self.filters:
            if event_type not in i.get_event_types():
                return False

        return True

    def get_result(self, event, values: Optional[dict[type, Any]] = None) -> bool:
        return all(i.get_result(event, values) for i in self.filters)


class DisjunctionEventFilter(AbstractEventBaseFilter):

    def __init__(self, *filters: AbstractEventBaseFilter):
        self.filters = filters

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(repr(i) for i in self.filters)})"

    def __iter__(self):
        return iter(self.filters)

    def __or__(self, other):
        if isinstance(other, DisjunctionEventFilter):
            return DisjunctionEventFilter(*self, *other)
        elif isinstance(other, AbstractEventBaseFilter):
            return DisjunctionEventFilter(*self, other)

        return NotImplemented

    def get_event_types(self) -> set[EventType]:
        types = set()

        for i in self.filters:
            types.update(i.get_event_types())

        return types

    def check_event_type(self, event_type: EventType) -> bool:
        for i in self.filters:
            if event_type not in i.get_event_types():
                return False

        return True

    def get_result(self, event, values: Optional[dict[type, Any]] = None) -> bool:
        return any(i.get_result(event, values) for i in self.filters)
