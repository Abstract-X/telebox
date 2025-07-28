from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class BotName(Type):
    name: str
