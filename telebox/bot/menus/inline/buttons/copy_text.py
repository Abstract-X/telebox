from telebox.bot.menus.inline.button import AbstractInlineButton
from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.bot.types.copy_text_button import CopyTextButton as CopyText


class CopyTextButton(AbstractInlineButton):
    def __init__(self, text: str, copy_text: CopyText):
        self.text = text
        self.copy_text = copy_text

    def get(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.text,
            copy_text=self.copy_text
        )
