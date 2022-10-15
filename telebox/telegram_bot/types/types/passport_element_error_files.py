from dataclasses import dataclass

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.consts import passport_element_error_sources


@dataclass(unsafe_hash=True)
class PassportElementErrorFiles(Type):
    type: str
    file_hashes: list[str]
    message: str
    source: str = passport_element_error_sources.FILES
