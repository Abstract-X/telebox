from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.consts import passport_element_error_sources


@define(repr=False)
class PassportElementErrorFrontSide(Type):
    type: str
    file_hash: str
    message: str
    source: str = passport_element_error_sources.FRONT_SIDE
