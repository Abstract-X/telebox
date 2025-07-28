from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class BotShortDescription(Type):
    short_description: str
