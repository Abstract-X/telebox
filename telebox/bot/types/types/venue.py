from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.location import Location


@dataclass
class Venue(Type):
    location: Location
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None
