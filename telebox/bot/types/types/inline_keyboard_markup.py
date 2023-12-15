from dataclasses import dataclass, field

from telebox.bot.types.type import Type
from telebox.bot.types.types.inline_keyboard_button import InlineKeyboardButton


@dataclass
class InlineKeyboardMarkup(Type):
    inline_keyboard: list[list[InlineKeyboardButton]] = field(default_factory=list)

    def __iter__(self):
        return iter(self.inline_keyboard)

    @property
    def rows(self) -> int:
        return len(self.inline_keyboard)

    def add_row(self, *buttons: InlineKeyboardButton) -> None:
        self.inline_keyboard.append(
            list(buttons)
        )

    def get_row_length(self, *, index: int = -1) -> int:
        return len(self.inline_keyboard[index])

    def add_in_row(self, button: InlineKeyboardButton, *, index: int = -1) -> None:
        self.inline_keyboard[index].append(button)
