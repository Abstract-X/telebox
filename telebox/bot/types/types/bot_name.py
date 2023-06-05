from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass
class BotName(Type):
    name: str
