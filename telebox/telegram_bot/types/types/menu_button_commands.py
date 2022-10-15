from dataclasses import dataclass

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.consts import menu_button_types


@dataclass(unsafe_hash=True)
class MenuButtonCommands(Type):
    type: str = menu_button_types.COMMANDS
