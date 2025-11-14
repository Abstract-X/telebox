from telebox.dialog_manager.reply.button import AbstractReplyButton
from telebox.bot.types.keyboard_button import KeyboardButton
from telebox.bot.types.keyboard_button_request_users import KeyboardButtonRequestUsers


class UserRequestButton(AbstractReplyButton):
    def __init__(
        self,
        text: str,
        request: KeyboardButtonRequestUsers
    ):
        self.text = text
        self.request = request

    def get(self) -> KeyboardButton:
        return KeyboardButton(text=self.text, request_users=self.request)
