from dataclasses import dataclass, field

from telebox.bot.types.type import Type
from telebox.bot.types.types.inline_keyboard_button import InlineKeyboardButton


@dataclass
class InlineKeyboardMarkup(Type):
    inline_keyboard: list[list[InlineKeyboardButton]] = field(default_factory=list)

    def add_row(self, *buttons: InlineKeyboardButton) -> None:
        self.inline_keyboard.append(
            list(buttons)
        )
