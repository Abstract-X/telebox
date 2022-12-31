from abc import ABC, abstractmethod

from telebox.dispatcher.enums.event_type import EventType


class AbstractEventBaseFilter(ABC):

    def __invert__(self):
        return InversionEventFilter(self)

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
    def check_event_type(self, event_type: EventType) -> bool:
        pass

    @abstractmethod
    def get_result(self, event, results: dict["AbstractEventBaseFilter", bool]) -> bool:
        pass


class AbstractEventFilter(AbstractEventBaseFilter, ABC):

    @abstractmethod
    def get_event_types(self) -> set[EventType]:
        pass

    @abstractmethod
    def check_event(self, event) -> bool:
        pass

    def check_event_type(self, event_type: EventType) -> bool:
        return event_type in self.get_event_types()

    def get_result(self, event, results: dict[AbstractEventBaseFilter, bool]) -> bool:
        try:
            result = results[self]
        except KeyError:
            result = results[self] = self.check_event(event)

        return result


class InversionEventFilter(AbstractEventBaseFilter):

    def __init__(self, filter_: AbstractEventBaseFilter):
        self.filter = filter_

    def __repr__(self):
        return f"{type(self).__name__}({self.filter!r})"

    def __invert__(self):
        return self.filter

    def check_event_type(self, event_type: EventType) -> bool:
        return self.filter.check_event_type(event_type)

    def get_result(self, event, results: dict[AbstractEventBaseFilter, bool]) -> bool:
        return not self.filter.get_result(event, results)


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

    def check_event_type(self, event_type: EventType) -> bool:
        return all(i.check_event_type(event_type) for i in self.filters)

    def get_result(self, event, results: dict[AbstractEventBaseFilter, bool]) -> bool:
        return all(i.get_result(event, results) for i in self.filters)


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

    def check_event_type(self, event_type: EventType) -> bool:
        return all(i.check_event_type(event_type) for i in self.filters)

    def get_result(self, event, results: dict[AbstractEventBaseFilter, bool]) -> bool:
        return any(i.get_result(event, results) for i in self.filters)
