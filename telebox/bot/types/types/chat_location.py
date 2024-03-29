from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.location import Location


@dataclass(repr=False)
class ChatLocation(Type):
    location: Location
    address: str
