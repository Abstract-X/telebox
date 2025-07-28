from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.business_opening_hours_interval import BusinessOpeningHoursInterval


@define(repr=False)
class BusinessOpeningHours(Type):
    time_zone_name: str
    opening_hours: list[BusinessOpeningHoursInterval]
