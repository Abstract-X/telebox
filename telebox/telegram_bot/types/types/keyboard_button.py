from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.types.types.keyboard_button_poll_type import KeyboardButtonPollType
from telebox.telegram_bot.types.types.web_app_info import WebAppInfo


@dataclass(unsafe_hash=True)
class KeyboardButton(Type):
    text: str
    request_contact: Optional[bool] = None
    request_location: Optional[bool] = None
    request_poll: Optional[KeyboardButtonPollType] = None
    web_app: Optional[WebAppInfo] = None
