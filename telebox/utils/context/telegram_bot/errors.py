from dataclasses import dataclass

from telebox.errors import TeleboxError
from telebox.typing import Event


@dataclass
class ContextTelegramBotError(TeleboxError):
    """General class for context telegram bot errors."""


@dataclass
class InvalidEventError(ContextTelegramBotError):
    event: Event
