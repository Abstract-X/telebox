from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.web_app_info import WebAppInfo
from telebox.bot.types.types.login_url import LoginUrl
from telebox.bot.types.types.callback_game import CallbackGame
from telebox.bot.types.types.switch_inline_query_chosen_chat import SwitchInlineQueryChosenChat


@dataclass(repr=False)
class InlineKeyboardButton(Type):
    text: str
    url: Optional[str] = None
    callback_data: Optional[str] = None
    web_app: Optional[WebAppInfo] = None
    login_url: Optional[LoginUrl] = None
    switch_inline_query: Optional[str] = None
    switch_inline_query_current_chat: Optional[str] = None
    switch_inline_query_chosen_chat: Optional[SwitchInlineQueryChosenChat] = None
    callback_game: Optional[CallbackGame] = None
    pay: Optional[bool] = None
