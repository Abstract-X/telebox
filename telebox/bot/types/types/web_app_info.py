from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(repr=False)
class WebAppInfo(Type):
    url: str
