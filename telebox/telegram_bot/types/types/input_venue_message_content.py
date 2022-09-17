from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.base import Type


@dataclass(unsafe_hash=True)
class InputVenueMessageContent(Type):
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None
