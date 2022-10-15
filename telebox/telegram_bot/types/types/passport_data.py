from dataclasses import dataclass

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.types.types.encrypted_passport_element import EncryptedPassportElement
from telebox.telegram_bot.types.types.encrypted_credentials import EncryptedCredentials


@dataclass(unsafe_hash=True)
class PassportData(Type):
    data: list[EncryptedPassportElement]
    credentials: EncryptedCredentials
