from typing import Union

from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.bot.menus.inline.button import AbstractInlineButton
from telebox.callback_data import get_callback_data
from telebox.unset import Unset, UNSET


class CallbackButton(AbstractInlineButton):
    def __init__(
        self,
        text: str,
        id_: int,
        *,
        payload: Union[str, int, float, bool, list, None] = None,
        icon_custom_emoji_id: Union[str, None, Unset] = UNSET,
        style: Union[str, None, Unset] = UNSET
    ):
        self.text = text
        self.id = id_
        self.payload = payload
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.style = style

    def get(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.text,
            callback_data=get_callback_data(
                id_=self.id,
                payload=self.payload
            ),
            icon_custom_emoji_id=self.icon_custom_emoji_id,
            style=self.style
        )
