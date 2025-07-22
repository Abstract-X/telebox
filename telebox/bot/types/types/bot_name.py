from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class BotName(Type):
    name: str
