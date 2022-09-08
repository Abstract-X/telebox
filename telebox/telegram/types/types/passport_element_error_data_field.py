from dataclasses import dataclass

from telebox.telegram.types.base import Type
from telebox.telegram.consts import passport_element_error_sources


@dataclass(unsafe_hash=True)
class PassportElementErrorDataField(Type):
    type: str
    field_name: str
    data_hash: str
    message: str
    source: str = passport_element_error_sources.DATA
