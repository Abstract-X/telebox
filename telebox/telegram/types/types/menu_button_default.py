from dataclasses import dataclass

from telebox.telegram.types.base import Type
from telebox.telegram.consts import menu_button_types


@dataclass(unsafe_hash=True)
class MenuButtonDefault(Type):
    type: str = menu_button_types.DEFAULT
