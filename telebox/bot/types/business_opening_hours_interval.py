from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class BusinessOpeningHoursInterval(Type):
    opening_minute: int
    closing_minute: int
