from typing import Optional

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.location import Location


@define(repr=False)
class Venue(Type):
    location: Location
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None
