from typing import Union, Optional

from telebox.ui.menu import Menu
from telebox.ui.reply.keyboard import ReplyKeyboard
from telebox.bot.types.input_media import InputMedia
from telebox.bot.types.message_entity import MessageEntity
from telebox.unset import Unset, UNSET


class ReplyMenu(Menu):
    def __init__(
        self,
        text: str,
        keyboard: ReplyKeyboard,
        media: Optional[InputMedia] = None,
        parse_mode: Union[str, None, Unset] = UNSET,
        entities: Union[list[MessageEntity], None, Unset] = UNSET
    ):
        super().__init__(
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            media=media
        )
        self.keyboard = keyboard
