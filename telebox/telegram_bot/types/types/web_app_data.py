from dataclasses import dataclass

from telebox.telegram_bot.types.base import Type


@dataclass(unsafe_hash=True)
class WebAppData(Type):
    data: str
    button_text: str
