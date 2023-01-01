from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.encrypted_passport_element import EncryptedPassportElement
from telebox.bot.types.types.encrypted_credentials import EncryptedCredentials


@dataclass(eq=False)
class PassportData(Type):
    data: list[EncryptedPassportElement]
    credentials: EncryptedCredentials
