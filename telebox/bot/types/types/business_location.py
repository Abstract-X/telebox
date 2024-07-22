from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.location import Location


@dataclass(repr=False)
class BusinessLocation(Type):
    address: str
    location: Optional[Location] = None
