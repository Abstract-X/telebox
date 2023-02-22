from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass
class EncryptedCredentials(Type):
    data: str
    hash: str
    secret: str
