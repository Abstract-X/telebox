from typing import Union, Optional

from telebox.bot.types.input_media import InputMedia
from telebox.bot.types.message_entity import MessageEntity
from telebox.unset import Unset, UNSET


class Menu:
    def __init__(
        self,
        text: str,
        media: Optional[InputMedia] = None,
        parse_mode: Union[str, None, Unset] = UNSET,
        entities: Union[list[MessageEntity], None, Unset] = UNSET
    ):
        self.text = text
        self.media = media
        self.parse_mode = parse_mode
        self.entities = entities
