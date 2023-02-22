from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass
class BotCommand(Type):
    command: str
    description: str
