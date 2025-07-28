from attrs import define, field

from telebox.bot.type import Type
from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton


@define(repr=False)
class InlineKeyboardMarkup(Type):
    inline_keyboard: list[list[InlineKeyboardButton]] = field(factory=list)

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
