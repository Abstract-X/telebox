from dataclasses import dataclass

from telebox.telegram.types.base import Type
from telebox.telegram.types.types.encrypted_passport_element import EncryptedPassportElement
from telebox.telegram.types.types.encrypted_credentials import EncryptedCredentials


@dataclass(unsafe_hash=True)
class PassportData(Type):
    data: list[EncryptedPassportElement]
    credentials: EncryptedCredentials
