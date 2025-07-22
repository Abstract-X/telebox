from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class BotCommand(Type):
    command: str
    description: str
