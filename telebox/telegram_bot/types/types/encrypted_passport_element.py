from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.base import Type
from telebox.telegram_bot.types.types.passport_file import PassportFile


@dataclass(unsafe_hash=True)
class EncryptedPassportElement(Type):
    type: str
    hash: str
    data: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    files: Optional[list[PassportFile]] = None
    front_side: Optional[PassportFile] = None
    reverse_side: Optional[PassportFile] = None
    selfie: Optional[PassportFile] = None
    translation: Optional[list[PassportFile]] = None
