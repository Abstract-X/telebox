from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class BotShortDescription(Type):
    short_description: str
