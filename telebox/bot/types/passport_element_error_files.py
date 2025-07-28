from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import passport_element_error_sources


@define(repr=False)
class PassportElementErrorFiles(Type):
    type: str
    file_hashes: list[str]
    message: str
    source: str = passport_element_error_sources.FILES
