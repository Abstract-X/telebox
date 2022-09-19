from dataclasses import dataclass

from telebox.telegram_bot.types.base import Type
from telebox.telegram_bot.types.types.location import Location


@dataclass(unsafe_hash=True)
class ChatLocation(Type):
    location: Location
    address: str
