from dataclasses import dataclass

from telebox.errors import TeleboxError


@dataclass
class EnvError(TeleboxError):
    """General class for env errors."""
