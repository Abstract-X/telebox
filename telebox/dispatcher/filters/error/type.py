from __future__ import annotations
from typing import Type, TYPE_CHECKING

from telebox.dispatcher.filters.error_filter import AbstractErrorFilter
if TYPE_CHECKING:
    from telebox.dispatcher.typing import Event


class ErrorTypeFilter(AbstractErrorFilter):

    def __init__(self, *types: Type[Exception], strictly: bool = False):
        if not types:
            raise ValueError("No types!")

        self._types = types
        self._strictly = strictly

    def get_value(self, error: Exception, event: Event) -> Exception:
        return error

    def check_value(self, value: Exception) -> bool:
        return type(value) in self._types if self._strictly else isinstance(value, self._types)
