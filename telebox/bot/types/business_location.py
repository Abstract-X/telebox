from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.location import Location


@define(repr=False)
class BusinessLocation(Type):
    address: str
    location: Optional[Location] = None
