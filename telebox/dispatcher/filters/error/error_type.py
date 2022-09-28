from typing import Type

from telebox.dispatcher.filters.base.error import AbstractErrorFilter
from telebox.typing import Event


class ErrorTypeFilter(AbstractErrorFilter):

    def __init__(self, *types: Type[Exception]):
        self._types = types

    def check(self, error: Exception, event: Event) -> bool:
        return isinstance(error, self._types)
