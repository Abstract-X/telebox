from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(unsafe_hash=True)
class BotCommand(Type):
    command: str
    description: str
