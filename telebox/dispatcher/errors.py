from dataclasses import dataclass

from telebox.errors import TeleboxError


@dataclass
class DispatcherError(TeleboxError):
    """General class for dispatcher errors."""


@dataclass
class PollingAlreadyStartedError(DispatcherError):
    """Class for error an already started polling."""
