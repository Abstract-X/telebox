from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass
class BotDescription(Type):
    description: str
