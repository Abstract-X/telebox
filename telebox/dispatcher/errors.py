from dataclasses import dataclass

from telebox.errors import TeleboxError


@dataclass
class DispatcherError(TeleboxError):
    """General class for dispatcher errors."""
