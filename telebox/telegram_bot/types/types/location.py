from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.base import Type


@dataclass(unsafe_hash=True)
class Location(Type):
    longitude: float
    latitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None
