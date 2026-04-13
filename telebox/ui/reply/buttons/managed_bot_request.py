from typing import Union

from telebox.bot.types.keyboard_button import KeyboardButton
from telebox.bot.types.keyboard_button_request_managed_bot import KeyboardButtonRequestManagedBot
from telebox.ui.reply.button import AbstractReplyButton
from telebox.unset import Unset, UNSET


class ManagedBotRequestButton(AbstractReplyButton):
    def __init__(
        self,
        text: str,
        request: KeyboardButtonRequestManagedBot,
        *,
        icon_custom_emoji_id: Union[str, None, Unset] = UNSET,
        style: Union[str, None, Unset] = UNSET
    ):
        self.text = text
        self.request = request
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.style = style

    def get(self) -> KeyboardButton:
        return KeyboardButton(
            text=self.text,
            request_managed_bot=self.request,
            icon_custom_emoji_id=self.icon_custom_emoji_id,
            style=self.style
        )
