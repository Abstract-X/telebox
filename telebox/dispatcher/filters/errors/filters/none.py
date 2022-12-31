from __future__ import annotations
from typing import TYPE_CHECKING

from telebox.dispatcher.filters.errors.filter import AbstractErrorFilter
if TYPE_CHECKING:
    from telebox.dispatcher.dispatcher import Event


class NoneErrorFilter(AbstractErrorFilter):

    def check_error(self, error: Exception, event: Event) -> bool:
        return True
