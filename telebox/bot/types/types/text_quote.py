from dataclasses import dataclass
from typing import Optional, Literal

from telebox.bot.types.type import Type
from telebox.bot.types.types.message_entity import MessageEntity


@dataclass
class TextQuote(Type):
    text: str
    position: int
    entities: Optional[list[MessageEntity]] = None
    is_manual: Optional[Literal[True]] = None
