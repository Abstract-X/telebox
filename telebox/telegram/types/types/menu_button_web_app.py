from dataclasses import dataclass

from telebox.telegram.types.base import Type
from telebox.telegram.consts import menu_button_types
from telebox.telegram.types.types.web_app_info import WebAppInfo


@dataclass(unsafe_hash=True)
class MenuButtonWebApp(Type):
    text: str
    web_app: WebAppInfo
    type: str = menu_button_types.WEB_APP
