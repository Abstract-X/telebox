from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type


@dataclass(eq=False)
class InputLocationMessageContent(Type):
    latitude: float
    longitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None
