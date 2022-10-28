from abc import ABC, abstractmethod
from typing import Optional, Any


class AbstractErrorBaseFilter(ABC):

    def __invert__(self):
        return InvertErrorFilter(self)

    def __and__(self, other):
        if isinstance(other, ConjunctionErrorFilter):
            return ConjunctionErrorFilter(self, *other)
        elif isinstance(other, AbstractErrorBaseFilter):
            return ConjunctionErrorFilter(self, other)

        return NotImplemented

    def __or__(self, other):
        if isinstance(other, DisjunctionErrorFilter):
            return DisjunctionErrorFilter(self, *other)
        elif isinstance(other, AbstractErrorBaseFilter):
            return DisjunctionErrorFilter(self, other)

        return NotImplemented

    @abstractmethod
    def get_result(self, error, event, values: Optional[dict[type, Any]] = None) -> bool:
        pass


class AbstractErrorFilter(AbstractErrorBaseFilter, ABC):

    @abstractmethod
    def get_value(self, error, event):
        pass

    @abstractmethod
    def check_value(self, value) -> bool:
        pass

    def get_result(self, error, event, values: Optional[dict[type, Any]] = None) -> bool:
        values = values or {}

        try:
            value = values[type(self)]
        except KeyError:
            value = values[type(self)] = self.get_value(error, event)

        return self.check_value(value)


class InvertErrorFilter(AbstractErrorBaseFilter):

    def __init__(self, filter_: AbstractErrorBaseFilter):
        self.filter = filter_

    def __repr__(self):
        return f"{type(self).__name__}({self.filter!r})"

    def __invert__(self):
        return self.filter

    def get_result(self, error, event, values: Optional[dict[type, Any]] = None) -> bool:
        return not self.filter.get_result(error, event, values)


class ConjunctionErrorFilter(AbstractErrorBaseFilter):

    def __init__(self, *filters: AbstractErrorBaseFilter):
        self.filters = filters

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(repr(i) for i in self.filters)})"

    def __iter__(self):
        return iter(self.filters)

    def __and__(self, other):
        if isinstance(other, ConjunctionErrorFilter):
            return ConjunctionErrorFilter(*self, *other)
        elif isinstance(other, AbstractErrorBaseFilter):
            return ConjunctionErrorFilter(*self, other)

        return NotImplemented

    def get_result(self, error, event, values: Optional[dict[type, Any]] = None) -> bool:
        return all(i.get_result(error, event, values) for i in self.filters)


class DisjunctionErrorFilter(AbstractErrorBaseFilter):

    def __init__(self, *filters: AbstractErrorBaseFilter):
        self.filters = filters

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(repr(i) for i in self.filters)})"

    def __iter__(self):
        return iter(self.filters)

    def __or__(self, other):
        if isinstance(other, DisjunctionErrorFilter):
            return DisjunctionErrorFilter(*self, *other)
        elif isinstance(other, AbstractErrorBaseFilter):
            return DisjunctionErrorFilter(*self, other)

        return NotImplemented

    def get_result(self, error, event, values: Optional[dict[type, Any]] = None) -> bool:
        return any(i.get_result(error, event, values) for i in self.filters)
