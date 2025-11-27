from telebox.bot.types.keyboard_button import KeyboardButton
from telebox.bot.types.web_app_info import WebAppInfo
from telebox.bot.menus.reply.button import AbstractReplyButton


class WebAppButton(AbstractReplyButton):
    def __init__(self, text: str, web_app: WebAppInfo):
        self.text = text
        self.web_app = web_app

    def get(self) -> KeyboardButton:
        return KeyboardButton(text=self.text, web_app=self.web_app)
