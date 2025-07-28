from typing import Optional

from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class InputLocationMessageContent(Type):
    latitude: float
    longitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None
