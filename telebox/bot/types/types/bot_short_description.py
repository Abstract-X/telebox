from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass
class BotShortDescription(Type):
    short_description: str
