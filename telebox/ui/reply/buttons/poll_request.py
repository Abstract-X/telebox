from typing import Union

from telebox.ui.reply.button import AbstractReplyButton
from telebox.bot.types.keyboard_button import KeyboardButton
from telebox.bot.types.keyboard_button_poll_type import KeyboardButtonPollType
from telebox.unset import Unset, UNSET


class PollRequestButton(AbstractReplyButton):
    def __init__(
        self,
        text: str,
        type_: KeyboardButtonPollType,
        *,
        icon_custom_emoji_id: Union[str, None, Unset] = UNSET,
        style: Union[str, None, Unset] = UNSET
    ):
        self.text = text
        self.type = type_
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.style = style

    def get(self) -> KeyboardButton:
        return KeyboardButton(
            text=self.text,
            request_poll=self.type,
            icon_custom_emoji_id=self.icon_custom_emoji_id,
            style=self.style
        )
