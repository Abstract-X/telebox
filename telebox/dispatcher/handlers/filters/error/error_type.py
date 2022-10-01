from typing import Type

from telebox.dispatcher.handlers.filters.base.error import AbstractErrorFilter
from telebox.typing import Event


class ErrorTypeFilter(AbstractErrorFilter):

    def __init__(self, *types: Type[Exception]):
        self._types = types

    def get_value(self, error: Exception, event: Event) -> Exception:
        return error

    def check_value(self, value: Exception) -> bool:
        return isinstance(value, self._types)
