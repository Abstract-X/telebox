from dataclasses import dataclass

from telebox.errors import TeleboxError


@dataclass
class UnknownFieldNameError(TeleboxError):
    name: str


@dataclass
class ClassNotFoundError(TeleboxError):
    field: str
