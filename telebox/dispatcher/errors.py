from dataclasses import dataclass

from telebox.errors import TeleboxError


@dataclass
class DispatcherError(TeleboxError):
    """Class for dispatcher errors."""
