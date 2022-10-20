from abc import ABC, abstractmethod


class AbstractFilter(ABC):

    def __invert__(self):
        return InvertFilter(self)

    def __and__(self, other):
        if isinstance(other, ConjunctionFilter):
            return ConjunctionFilter(self, *other)
        elif isinstance(other, AbstractFilter):
            return ConjunctionFilter(self, other)

        return NotImplemented

    def __or__(self, other):
        if isinstance(other, DisjunctionFilter):
            return DisjunctionFilter(self, *other)
        elif isinstance(other, AbstractFilter):
            return DisjunctionFilter(self, other)

        return NotImplemented

    @abstractmethod
    def get_result(self, *args, **kwargs) -> bool:
        pass


class AbstractValueFilter(AbstractFilter):

    @abstractmethod
    def get_value(self, *args, **kwargs):
        pass

    @abstractmethod
    def check_value(self, value) -> bool:
        pass


class AbstractSingleFilter(AbstractFilter, ABC):

    def __init__(self, filter_: AbstractFilter):
        self.filter = filter_

    def __repr__(self):
        return f"{type(self).__name__}({self.filter!r})"


class AbstractMultipleFilter(AbstractFilter, ABC):

    def __init__(self, *filters: AbstractFilter):
        self.filters = filters

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(repr(i) for i in self.filters)})"

    def __iter__(self):
        return iter(self.filters)


class InvertFilter(AbstractSingleFilter):

    def __invert__(self):
        return self.filter

    def get_result(self, *args, **kwargs) -> bool:
        return not self.filter.get_result(*args, **kwargs)


class ConjunctionFilter(AbstractMultipleFilter):

    def __and__(self, other):
        if isinstance(other, ConjunctionFilter):
            return ConjunctionFilter(*self, *other)
        elif isinstance(other, AbstractFilter):
            return ConjunctionFilter(*self, other)

        return NotImplemented

    def get_result(self, *args, **kwargs) -> bool:
        return all(i.get_result(*args, **kwargs) for i in self.filters)


class DisjunctionFilter(AbstractMultipleFilter):

    def __or__(self, other):
        if isinstance(other, DisjunctionFilter):
            return DisjunctionFilter(*self, *other)
        elif isinstance(other, AbstractFilter):
            return DisjunctionFilter(*self, other)

        return NotImplemented

    def get_result(self, *args, **kwargs) -> bool:
        return any(i.get_result(*args, **kwargs) for i in self.filters)
