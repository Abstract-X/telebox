from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.keyboard_button_request_users import KeyboardButtonRequestUsers
from telebox.bot.types.types.keyboard_button_request_chat import KeyboardButtonRequestChat
from telebox.bot.types.types.keyboard_button_poll_type import KeyboardButtonPollType
from telebox.bot.types.types.web_app_info import WebAppInfo


@dataclass(repr=False)
class KeyboardButton(Type):
    text: str
    request_users: Optional[KeyboardButtonRequestUsers] = None
    request_chat: Optional[KeyboardButtonRequestChat] = None
    request_contact: Optional[bool] = None
    request_location: Optional[bool] = None
    request_poll: Optional[KeyboardButtonPollType] = None
    web_app: Optional[WebAppInfo] = None
