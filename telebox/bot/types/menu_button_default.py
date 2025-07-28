from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import menu_button_types


@define(repr=False)
class MenuButtonDefault(Type):
    type: str = menu_button_types.DEFAULT
