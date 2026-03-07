from typing import Union

from telebox.bot.types.keyboard_button import KeyboardButton
from telebox.bot.types.web_app_info import WebAppInfo
from telebox.bot.menus.reply.button import AbstractReplyButton
from telebox.unset import Unset, UNSET


class WebAppButton(AbstractReplyButton):
    def __init__(
        self,
        text: str,
        web_app: WebAppInfo,
        *,
        icon_custom_emoji_id: Union[str, None, Unset] = UNSET,
        style: Union[str, None, Unset] = UNSET
    ):
        self.text = text
        self.web_app = web_app
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.style = style

    def get(self) -> KeyboardButton:
        return KeyboardButton(
            text=self.text,
            web_app=self.web_app,
            icon_custom_emoji_id=self.icon_custom_emoji_id,
            style=self.style
        )
