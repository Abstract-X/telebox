from typing import Union

from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.ui.inline.button import AbstractInlineButton
from telebox.unset import Unset, UNSET


class QueryButton(AbstractInlineButton):
    def __init__(
        self,
        text: str,
        query: str,
        *,
        icon_custom_emoji_id: Union[str, None, Unset] = UNSET,
        style: Union[str, None, Unset] = UNSET
    ):
        self.text = text
        self.query = query
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.style = style

    def get(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.text,
            switch_inline_query=self.query,
            icon_custom_emoji_id=self.icon_custom_emoji_id,
            style=self.style
        )
