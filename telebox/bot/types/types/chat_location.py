from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.location import Location


@dataclass(unsafe_hash=True)
class ChatLocation(Type):
    location: Location
    address: str
