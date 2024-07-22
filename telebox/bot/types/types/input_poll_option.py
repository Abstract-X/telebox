from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.message_entity import MessageEntity


@dataclass(repr=False)
class InputPollOption(Type):
    text: str
    text_parse_mode: Optional[str] = None
    text_entities: Optional[list[MessageEntity]] = None
