from typing import Optional

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.location import Location


@define(repr=False)
class BusinessLocation(Type):
    address: str
    location: Optional[Location] = None
