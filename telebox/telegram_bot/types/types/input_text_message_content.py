from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.base import Type
from telebox.telegram_bot.types.types.message_entity import MessageEntity


@dataclass(unsafe_hash=True)
class InputTextMessageContent(Type):
    message_text: str
    parse_mode: Optional[str] = None
    entities: Optional[list[MessageEntity]] = None
    disable_web_page_preview: Optional[bool] = None
