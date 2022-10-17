from dataclasses import dataclass

from telebox.errors import TeleboxError
from telebox.dispatcher.dispatcher import Event


@dataclass
class ContextError(TeleboxError):
    """General class for context errors."""


@dataclass
class InvalidEventError(ContextError):
    event: Event
