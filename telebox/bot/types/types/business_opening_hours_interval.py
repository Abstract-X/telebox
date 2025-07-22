from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class BusinessOpeningHoursInterval(Type):
    opening_minute: int
    closing_minute: int
