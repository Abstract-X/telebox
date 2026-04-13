from typing import Union

from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.ui.inline.button import AbstractInlineButton
from telebox.unset import Unset, UNSET


class LinkButton(AbstractInlineButton):
    def __init__(
        self,
        text: str,
        url: str,
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
            url=self.url,
            icon_custom_emoji_id=self.icon_custom_emoji_id,
            style=self.style
        )
