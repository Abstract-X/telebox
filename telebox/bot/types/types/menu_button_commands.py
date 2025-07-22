from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.consts import menu_button_types


@define(repr=False)
class MenuButtonCommands(Type):
    type: str = menu_button_types.COMMANDS
