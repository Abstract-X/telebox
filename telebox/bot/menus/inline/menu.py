from typing import Union, Optional

from telebox.bot.menu import Menu
from telebox.bot.menus.inline.keyboard import InlineKeyboard
from telebox.bot.types.input_media import InputMedia
from telebox.bot.types.message_entity import MessageEntity
from telebox.unset import Unset, UNSET


class InlineMenu(Menu):
    def __init__(
        self,
        text: str,
        keyboard: InlineKeyboard,
        media: Optional[InputMedia] = None,
        parse_mode: Union[str, None, Unset] = UNSET,
        entities: Union[list[MessageEntity], None, Unset] = UNSET
    ):
        super().__init__(
            text=text,
            media=media,
            parse_mode=parse_mode,
            entities=entities
        )
        self.keyboard = keyboard
