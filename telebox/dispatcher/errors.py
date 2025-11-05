from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from telebox.errors import TeleboxError
if TYPE_CHECKING:
    from telebox.dispatcher.type_hints import Event


@dataclass
class DispatcherError(TeleboxError):
    """Class for dispatcher errors."""


@dataclass
class InvalidEventError(DispatcherError):
    event: Event
