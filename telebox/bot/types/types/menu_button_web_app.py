from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.consts import menu_button_types
from telebox.bot.types.types.web_app_info import WebAppInfo


@define(repr=False)
class MenuButtonWebApp(Type):
    text: str
    web_app: WebAppInfo
    type: str = menu_button_types.WEB_APP
