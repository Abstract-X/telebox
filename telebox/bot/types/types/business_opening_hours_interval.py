from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(repr=False)
class BusinessOpeningHoursInterval(Type):
    opening_minute: int
    closing_minute: int
