from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.message_entity import MessageEntity


@dataclass(repr=False)
class PollOption(Type):
    text: str
    voter_count: int
    text_entities: Optional[MessageEntity] = None
