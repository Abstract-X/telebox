from telebox.bot.menus.reply.button import AbstractReplyButton
from telebox.bot.types.keyboard_button import KeyboardButton
from telebox.bot.types.keyboard_button_poll_type import KeyboardButtonPollType


class PollRequestButton(AbstractReplyButton):
    def __init__(
        self,
        text: str,
        type_: KeyboardButtonPollType
    ):
        self.text = text
        self.type = type_

    def get(self) -> KeyboardButton:
        return KeyboardButton(text=self.text, request_poll=self.type)
