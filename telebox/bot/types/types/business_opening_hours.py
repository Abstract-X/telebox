from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.business_opening_hours_interval import BusinessOpeningHoursInterval


@dataclass(repr=False)
class BusinessOpeningHours(Type):
    time_zone_name: str
    opening_hours: list[BusinessOpeningHoursInterval]
