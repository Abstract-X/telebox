from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import passport_element_error_sources


@dataclass(repr=False)
class PassportElementErrorFile(Type):
    type: str
    file_hash: str
    message: str
    source: str = passport_element_error_sources.FILE
