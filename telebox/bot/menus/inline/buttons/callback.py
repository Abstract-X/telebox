from typing import Union

from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.bot.menus.inline.button import AbstractInlineButton
from telebox.utils.callback_data import get_callback_data


class CallbackButton(AbstractInlineButton):
    def __init__(
        self,
        text: str,
        id_: int,
        payload: Union[str, int, float, bool, list, None] = None
    ):
        self.text = text
        self.id = id_
        self.payload = payload

    def get(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.text,
            callback_data=get_callback_data(
                id_=self.id,
                payload=self.payload
            )
        )
