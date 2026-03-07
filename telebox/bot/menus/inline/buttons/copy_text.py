from typing import Union

from telebox.bot.menus.inline.button import AbstractInlineButton
from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.bot.types.copy_text_button import CopyTextButton as CopyText
from telebox.unset import Unset, UNSET


class CopyTextButton(AbstractInlineButton):
    def __init__(
        self,
        text: str,
        copy_text: CopyText,
        *,
        icon_custom_emoji_id: Union[str, None, Unset] = UNSET,
        style: Union[str, None, Unset] = UNSET
    ):
        self.text = text
        self.copy_text = copy_text
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.style = style

    def get(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.text,
            copy_text=self.copy_text,
            icon_custom_emoji_id=self.icon_custom_emoji_id,
            style=self.style
        )
