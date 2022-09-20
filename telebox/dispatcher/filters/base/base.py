from abc import ABC, abstractmethod


class AbstractFilter(ABC):

    def __invert__(self):
        return InvertedFilter(self)

    def __and__(self, other):
        return AllFilter(self, other)

    def __or__(self, other):
        return AnyFilter(self, other)

    @abstractmethod
    def check(self, *args, **kwargs) -> bool:
        pass


class InvertedFilter(AbstractFilter):

    def __init__(self, filter_: AbstractFilter):
        self._filter = filter_

    def check(self, *args, **kwargs) -> bool:
        return not self._filter.check(*args, **kwargs)


class AllFilter(AbstractFilter):

    def __init__(self, *filters: AbstractFilter):
        self._filters = set(filters)

    def __and__(self, other):
        return AllFilter(*self._filters, other)

    def check(self, *args, **kwargs) -> bool:
        return all(i.check(*args, **kwargs) for i in self._filters)


class AnyFilter(AbstractFilter):

    def __init__(self, *filters: AbstractFilter):
        self._filters = set(filters)

    def __or__(self, other):
        return AnyFilter(*self._filters, other)

    def check(self, *args, **kwargs) -> bool:
        return any(i.check(*args, **kwargs) for i in self._filters)
