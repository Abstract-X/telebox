from dataclasses import dataclass

from telebox.errors import TeleboxError


@dataclass
class DepsError(TeleboxError):
    """Class for deps errors."""
