from dataclasses import dataclass

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.consts import menu_button_types
from telebox.telegram_bot.types.types.web_app_info import WebAppInfo


@dataclass(unsafe_hash=True)
class MenuButtonWebApp(Type):
    text: str
    web_app: WebAppInfo
    type: str = menu_button_types.WEB_APP
