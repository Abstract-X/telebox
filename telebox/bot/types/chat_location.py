from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.location import Location


@define(repr=False)
class ChatLocation(Type):
    location: Location
    address: str
