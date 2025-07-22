from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.location import Location


@define(repr=False)
class ChatLocation(Type):
    location: Location
    address: str
