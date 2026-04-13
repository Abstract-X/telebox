from typing import Union

from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.bot.types.switch_inline_query_chosen_chat import SwitchInlineQueryChosenChat
from telebox.ui.inline.button import AbstractInlineButton
from telebox.unset import Unset, UNSET


class ChosenChatQueryButton(AbstractInlineButton):
    def __init__(
        self,
        text: str,
        query: SwitchInlineQueryChosenChat,
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
            switch_inline_query_chosen_chat=self.query,
            icon_custom_emoji_id=self.icon_custom_emoji_id,
            style=self.style
        )
