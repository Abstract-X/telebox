from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import menu_button_types


@dataclass(unsafe_hash=True)
class MenuButtonDefault(Type):
    type: str = menu_button_types.DEFAULT
