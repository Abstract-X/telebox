from abc import ABC, abstractmethod
from contextvars import ContextVar  # noqa

from telebox.dispatcher.enums.event_type import EventType


class AbstractBaseFilter(ABC):

    def __invert__(self):
        return InversionFilter(self)

    def __and__(self, other):
        if isinstance(other, ConjunctionFilter):
            return ConjunctionFilter(self, *other)
        elif isinstance(other, AbstractBaseFilter):
            return ConjunctionFilter(self, other)

        return NotImplemented

    def __or__(self, other):
        if isinstance(other, DisjunctionFilter):
            return DisjunctionFilter(self, *other)
        elif isinstance(other, AbstractBaseFilter):
            return DisjunctionFilter(self, other)

        return NotImplemented

    @abstractmethod
    def check_event_type(self, event_type: EventType) -> bool:
        pass

    @abstractmethod
    def get_result(self, event) -> bool:
        pass


class AbstractFilter(AbstractBaseFilter, ABC):

    def __init_subclass__(cls, **kwargs):
        unique_name = f"{cls.__module__}.{cls.__qualname__}"
        cls.__event_context = ContextVar(f"{unique_name}_event_context", default=None)
        cls.__value_context = ContextVar(f"{unique_name}_value_context")

    @abstractmethod
    def get_event_types(self) -> set[EventType]:
        pass

    @abstractmethod
    def get_value(self, event):
        pass

    @abstractmethod
    def check_value(self, value) -> bool:
        pass

    def check_event_type(self, event_type: EventType) -> bool:
        return event_type in self.get_event_types()

    def get_result(self, event) -> bool:
        cached_event = self.__event_context.get()

        if event is cached_event:
            value = self.__value_context.get()
        else:
            value = self.__set_context(event)

        return self.check_value(value)

    def __set_context(self, event):
        value = self.get_value(event)
        self.__event_context.set(event)
        self.__value_context.set(value)

        return value


class InversionFilter(AbstractBaseFilter):

    def __init__(self, filter_: AbstractBaseFilter):
        self.filter = filter_

    def __repr__(self):
        return f"{type(self).__name__}({self.filter!r})"

    def __invert__(self):
        return self.filter

    def check_event_type(self, event_type: EventType) -> bool:
        return self.filter.check_event_type(event_type)

    def get_result(self, event) -> bool:
        return not self.filter.get_result(event)


class ConjunctionFilter(AbstractBaseFilter):

    def __init__(self, *filters: AbstractBaseFilter):
        self.filters = filters

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(repr(i) for i in self.filters)})"

    def __iter__(self):
        return iter(self.filters)

    def __and__(self, other):
        if isinstance(other, ConjunctionFilter):
            return ConjunctionFilter(*self, *other)
        elif isinstance(other, AbstractBaseFilter):
            return ConjunctionFilter(*self, other)

        return NotImplemented

    def check_event_type(self, event_type: EventType) -> bool:
        return all(i.check_event_type(event_type) for i in self.filters)

    def get_result(self, event) -> bool:
        return all(i.get_result(event) for i in self.filters)


class DisjunctionFilter(AbstractBaseFilter):

    def __init__(self, *filters: AbstractBaseFilter):
        self.filters = filters

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(repr(i) for i in self.filters)})"

    def __iter__(self):
        return iter(self.filters)

    def __or__(self, other):
        if isinstance(other, DisjunctionFilter):
            return DisjunctionFilter(*self, *other)
        elif isinstance(other, AbstractBaseFilter):
            return DisjunctionFilter(*self, other)

        return NotImplemented

    def check_event_type(self, event_type: EventType) -> bool:
        return all(i.check_event_type(event_type) for i in self.filters)

    def get_result(self, event) -> bool:
        return any(i.get_result(event) for i in self.filters)
