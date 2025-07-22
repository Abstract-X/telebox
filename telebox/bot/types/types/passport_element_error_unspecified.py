from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.consts import passport_element_error_sources


@define(repr=False)
class PassportElementErrorUnspecified(Type):
    type: str
    element_hash: str
    message: str
    source: str = passport_element_error_sources.UNSPECIFIED
