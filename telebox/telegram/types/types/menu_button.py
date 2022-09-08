from typing import Union

from telebox.telegram.types.types.menu_button_commands import MenuButtonCommands
from telebox.telegram.types.types.menu_button_web_app import MenuButtonWebApp
from telebox.telegram.types.types.menu_button_default import MenuButtonDefault


MenuButton = Union[MenuButtonCommands,
                   MenuButtonWebApp,
                   MenuButtonDefault]
