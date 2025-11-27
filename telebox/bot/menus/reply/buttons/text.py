from telebox.bot.types.keyboard_button import KeyboardButton
from telebox.bot.menus.reply.button import AbstractReplyButton


class TextButton(AbstractReplyButton):
    def __init__(self, text: str):
        self.text = text

    def get(self) -> KeyboardButton:
        return KeyboardButton(text=self.text)
