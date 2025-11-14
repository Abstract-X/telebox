from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.dialog_manager.inline.button import AbstractInlineButton


class LinkButton(AbstractInlineButton):
    def __init__(self, text: str, url: str):
        self.text = text
        self.url = url

    def get(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(text=self.text, url=self.url)
