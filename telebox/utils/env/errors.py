from dataclasses import dataclass

from telebox.errors import TeleboxError


@dataclass
class EnvError(TeleboxError):
    """Class for env errors."""
