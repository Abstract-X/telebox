from telebox.bot.types.keyboard_button import KeyboardButton
from telebox.bot.types.keyboard_button_request_chat import KeyboardButtonRequestChat
from telebox.bot.menus.reply.button import AbstractReplyButton


class ChatRequestButton(AbstractReplyButton):
    def __init__(
        self,
        text: str,
        request: KeyboardButtonRequestChat
    ):
        self.text = text
        self.request = request

    def get(self) -> KeyboardButton:
        return KeyboardButton(text=self.text, request_chat=self.request)
