from typing import Union

from telebox.ui.inline.button import AbstractInlineButton
from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.bot.types.login_url import LoginUrl
from telebox.unset import Unset, UNSET


class LoginButton(AbstractInlineButton):
    def __init__(
        self,
        text: str,
        url: LoginUrl,
        *,
        icon_custom_emoji_id: Union[str, None, Unset] = UNSET,
        style: Union[str, None, Unset] = UNSET
    ):
        self.text = text
        self.url = url
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.style = style

    def get(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.text,
            login_url=self.url,
            icon_custom_emoji_id=self.icon_custom_emoji_id,
            style=self.style
        )
