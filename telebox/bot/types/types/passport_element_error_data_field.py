from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import passport_element_error_sources


@dataclass(unsafe_hash=True)
class PassportElementErrorDataField(Type):
    type: str
    field_name: str
    data_hash: str
    message: str
    source: str = passport_element_error_sources.DATA
