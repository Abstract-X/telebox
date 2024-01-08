from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.message_entity import MessageEntity
from telebox.bot.types.types.link_preview_options import LinkPreviewOptions


@dataclass
class InputTextMessageContent(Type):
    message_text: str
    parse_mode: Optional[str] = None
    entities: Optional[list[MessageEntity]] = None
    link_preview_options: Optional[LinkPreviewOptions] = None
