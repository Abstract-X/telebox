from typing import Optional

from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class Location(Type):
    longitude: float
    latitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None
