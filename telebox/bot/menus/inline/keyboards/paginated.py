from typing import Optional

from telebox.bot.menus.inline.keyboard import InlineKeyboard
from telebox.bot.menus.inline.button import AbstractInlineButton
from telebox.bot.menus.inline.buttons.callback import CallbackButton


class PaginatedInlineKeyboard(InlineKeyboard):
    def __init__(
        self,
        buttons: list[AbstractInlineButton],
        total_pages: int,
        previous_page_button: CallbackButton,
        next_page_button: CallbackButton,
        page_button: Optional[CallbackButton] = None,
        start_page_button: Optional[CallbackButton] = None,
        end_page_button: Optional[CallbackButton] = None,
        width: int = 1
    ):
        super().__init__()

        for row in (buttons[i:i + width] for i in range(0, len(buttons), width)):
            self.add_row(*row)

        if total_pages == 1:
            return

        self.add_row()

        if start_page_button is not None:
            self.add_in_row(start_page_button)

        self.add_in_row(previous_page_button)

        if page_button is not None:
            self.add_in_row(page_button)

        self.add_in_row(next_page_button)

        if end_page_button is not None:
            self.add_in_row(end_page_button)
