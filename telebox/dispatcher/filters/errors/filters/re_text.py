from __future__ import annotations
from typing import Pattern, TYPE_CHECKING

from telebox.dispatcher.filters.errors.filter import AbstractErrorFilter
if TYPE_CHECKING:
    from telebox.dispatcher.typing import Event


class RETextErrorFilter(AbstractErrorFilter):

    def __init__(self, *patterns: Pattern, full_match: bool = True):
        if not patterns:
            raise ValueError("No patterns!")

        self._patterns = set(patterns)
        self._full_match = full_match

    def check_error(self, error: Exception, event: Event) -> bool:
        text = str(error)

        if self._full_match:
            return any(i.fullmatch(text) is not None for i in self._patterns)
        else:
            return any(i.search(text) is not None for i in self._patterns)
