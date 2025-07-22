from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class EncryptedCredentials(Type):
    data: str
    hash: str
    secret: str
