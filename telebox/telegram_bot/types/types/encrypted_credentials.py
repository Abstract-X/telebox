from dataclasses import dataclass

from telebox.telegram_bot.types.type import Type


@dataclass(unsafe_hash=True)
class EncryptedCredentials(Type):
    data: str
    hash: str
    secret: str
