from dataclasses import dataclass, field
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.keyboard_button import KeyboardButton


@dataclass
class ReplyKeyboardMarkup(Type):
    keyboard: list[list[KeyboardButton]] = field(default_factory=list)
    is_persistent: Optional[bool] = None
    resize_keyboard: Optional[bool] = None
    one_time_keyboard: Optional[bool] = None
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None

    def add_row(self, *buttons: KeyboardButton) -> None:
        self.keyboard.append(
            list(buttons)
        )
