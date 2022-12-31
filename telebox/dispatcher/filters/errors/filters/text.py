from __future__ import annotations
from typing import TYPE_CHECKING

from telebox.dispatcher.filters.errors.filter import AbstractErrorFilter
if TYPE_CHECKING:
    from telebox.dispatcher.typing import Event


class TextErrorFilter(AbstractErrorFilter):

    def __init__(self, *texts: str, full_match: bool = True, ignore_case: bool = False):
        if not texts:
            raise ValueError("No texts!")

        self._texts = {i.lower() for i in texts} if ignore_case else set(texts)
        self._full_match = full_match
        self._ignore_case = ignore_case

    def check_error(self, error: Exception, event: Event) -> bool:
        text = str(error)

        if self._ignore_case:
            text = text.lower()

        if self._full_match:
            return text in self._texts
        else:
            return any(i in text for i in self._texts)
