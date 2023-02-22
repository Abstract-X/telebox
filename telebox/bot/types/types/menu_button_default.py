from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.consts import menu_button_types


@dataclass
class MenuButtonDefault(Type):
    type: str = menu_button_types.DEFAULT
