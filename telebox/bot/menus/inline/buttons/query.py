from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.bot.menus.inline.button import AbstractInlineButton


class QueryButton(AbstractInlineButton):
    def __init__(self, text: str, query: str):
        self.text = text
        self.query = query

    def get(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(text=self.text, switch_inline_query=self.query)
