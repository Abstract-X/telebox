from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.encrypted_passport_element import EncryptedPassportElement
from telebox.bot.types.types.encrypted_credentials import EncryptedCredentials


@define(repr=False)
class PassportData(Type):
    data: list[EncryptedPassportElement]
    credentials: EncryptedCredentials
