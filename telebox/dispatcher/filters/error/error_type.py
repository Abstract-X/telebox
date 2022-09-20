from typing import Type

from telebox.dispatcher.filters.base.error import AbstractErrorFilter
from telebox.typing import Event


class ErrorTypeFilter(AbstractErrorFilter):

    def __init__(self, *types: Type[Exception]):
        self._types = set(types)

    def check_error(self, error: Exception, event: Event) -> bool:
        for type_ in self._types:
            if isinstance(error, type_):
                return True

        return False
