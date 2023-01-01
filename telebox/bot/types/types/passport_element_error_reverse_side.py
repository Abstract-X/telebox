from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import passport_element_error_sources


@dataclass(eq=False)
class PassportElementErrorReverseSide(Type):
    type: str
    file_hash: str
    message: str
    source: str = passport_element_error_sources.REVERSE_SIDE
