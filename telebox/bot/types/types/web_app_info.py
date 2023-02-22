from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass
class WebAppInfo(Type):
    url: str
