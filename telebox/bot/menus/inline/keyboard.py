from typing import Optional

from telebox.bot.menus.inline.button import AbstractInlineButton
from telebox.bot.types.inline_keyboard_markup import InlineKeyboardMarkup


class InlineKeyboard:
    def __init__(self, buttons: Optional[list[list[AbstractInlineButton]]] = None):
        self.buttons = buttons or []

    @property
    def rows(self) -> int:
        return len(self.buttons)

    def get_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [button.get() for button in row]
                for row in self.buttons
            ]
        )

    def add_row(self, *buttons: AbstractInlineButton) -> None:
        self.buttons.append(
            list(buttons)
        )

    def get_row_length(self, *, index: int = -1) -> int:
        return len(self.buttons[index])

    def add_in_row(self, button: AbstractInlineButton, *, index: int = -1) -> None:
        self.buttons[index].append(button)
