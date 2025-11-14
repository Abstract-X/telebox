from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.bot.types.web_app_info import WebAppInfo
from telebox.dialog_manager.inline.button import AbstractInlineButton


class WebAppButton(AbstractInlineButton):
    def __init__(self, text: str, web_app: WebAppInfo):
        self.text = text
        self.web_app = web_app

    def get(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(text=self.text, web_app=self.web_app)
