from telebox.dispatcher.router import Router
from telebox.dialog_manager.keyboard import AbstractKeyboard
from telebox.dialog_manager.inline.button import AbstractInlineButton
from telebox.bot.types.inline_keyboard_markup import InlineKeyboardMarkup


class InlineKeyboard(AbstractKeyboard):
    def __init__(self, buttons: list[list[AbstractInlineButton]]):
        self.buttons = buttons

    def get(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [button.get() for button in row]
                for row in self.buttons
            ]
        )

    def set_handlers(self, router: Router) -> None:
        for row in self.buttons:
            for button in row:
                button.set_handler(router=router)
