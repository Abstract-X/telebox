from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.message_entity import MessageEntity


@dataclass
class InputTextMessageContent(Type):
    message_text: str
    parse_mode: Optional[str] = None
    entities: Optional[list[MessageEntity]] = None
    disable_web_page_preview: Optional[bool] = None
