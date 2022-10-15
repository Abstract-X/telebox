from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.types.types.keyboard_button import KeyboardButton


@dataclass(unsafe_hash=True)
class ReplyKeyboardMarkup(Type):
    keyboard: list[list[KeyboardButton]]
    resize_keyboard: Optional[bool] = None
    one_time_keyboard: Optional[bool] = None
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None
