from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(eq=False)
class BotCommand(Type):
    command: str
    description: str
