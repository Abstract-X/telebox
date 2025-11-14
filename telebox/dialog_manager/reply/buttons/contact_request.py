from telebox.bot.types.keyboard_button import KeyboardButton
from telebox.dialog_manager.reply.button import AbstractReplyButton


class ContactRequestButton(AbstractReplyButton):
    def __init__(self, text: str):
        self.text = text

    def get(self) -> KeyboardButton:
        return KeyboardButton(text=self.text, request_contact=True)
