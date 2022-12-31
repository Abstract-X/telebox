from __future__ import annotations
from typing import Type, TYPE_CHECKING

from telebox.dispatcher.filters.errors.filter import AbstractErrorFilter
if TYPE_CHECKING:
    from telebox.dispatcher.typing import Event


class TypeErrorFilter(AbstractErrorFilter):

    def __init__(self, *types: Type[Exception], strictly: bool = False):
        if not types:
            raise ValueError("No types!")

        self._types = types
        self._strictly = strictly

    def check_error(self, error: Exception, event: Event) -> bool:
        return type(error) in self._types if self._strictly else isinstance(error, self._types)
