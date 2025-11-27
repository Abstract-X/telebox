from telebox.bot.menus.inline.button import AbstractInlineButton
from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.bot.types.login_url import LoginUrl


class LoginButton(AbstractInlineButton):
    def __init__(self, text: str, url: LoginUrl):
        self.text = text
        self.url = url

    def get(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(text=self.text, login_url=self.url)
