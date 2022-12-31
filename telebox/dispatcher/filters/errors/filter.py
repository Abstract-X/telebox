from abc import ABC, abstractmethod


class AbstractErrorBaseFilter(ABC):

    def __invert__(self):
        return InversionErrorFilter(self)

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
    def get_result(self, error, event, results: dict["AbstractErrorBaseFilter", bool]) -> bool:
        pass


class AbstractErrorFilter(AbstractErrorBaseFilter, ABC):

    @abstractmethod
    def check_error(self, error, event) -> bool:
        pass

    def get_result(self, error, event, results: dict[AbstractErrorBaseFilter, bool]) -> bool:
        try:
            result = results[self]
        except KeyError:
            result = results[self] = self.check_error(error, event)

        return result


class InversionErrorFilter(AbstractErrorBaseFilter):

    def __init__(self, filter_: AbstractErrorBaseFilter):
        self.filter = filter_

    def __repr__(self):
        return f"{type(self).__name__}({self.filter!r})"

    def __invert__(self):
        return self.filter

    def get_result(self, error, event, results: dict[AbstractErrorBaseFilter, bool]) -> bool:
        return not self.filter.get_result(error, event, results)


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

    def get_result(self, error, event, results: dict[AbstractErrorBaseFilter, bool]) -> bool:
        return all(i.get_result(error, event, results) for i in self.filters)


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

    def get_result(self, error, event, results: dict[AbstractErrorBaseFilter, bool]) -> bool:
        return any(i.get_result(error, event, results) for i in self.filters)
