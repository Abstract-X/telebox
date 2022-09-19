from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.base import Type
from telebox.telegram_bot.types.types.web_app_info import WebAppInfo
from telebox.telegram_bot.types.types.login_url import LoginUrl
from telebox.telegram_bot.types.types.callback_game import CallbackGame


@dataclass(unsafe_hash=True)
class InlineKeyboardButton(Type):
    text: str
    url: Optional[str] = None
    callback_data: Optional[str] = None
    web_app: Optional[WebAppInfo] = None
    login_url: Optional[LoginUrl] = None
    switch_inline_query: Optional[str] = None
    switch_inline_query_current_chat: Optional[str] = None
    callback_game: Optional[CallbackGame] = None
    pay: Optional[bool] = None
