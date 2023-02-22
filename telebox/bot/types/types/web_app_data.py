from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass
class WebAppData(Type):
    data: str
    button_text: str
