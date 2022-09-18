from dataclasses import dataclass

from telebox.telegram_bot.types.base import Type
from telebox.telegram_bot.consts import passport_element_error_sources


@dataclass(unsafe_hash=True)
class PassportElementErrorFile(Type):
    type: str
    file_hash: str
    message: str
    source: str = passport_element_error_sources.FILE