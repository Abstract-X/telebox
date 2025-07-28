from typing import Optional, Literal

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.message_entity import MessageEntity


@define(repr=False)
class TextQuote(Type):
    text: str
    position: int
    entities: Optional[list[MessageEntity]] = None
    is_manual: Optional[Literal[True]] = None
