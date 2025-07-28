from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.message_entity import MessageEntity


@define(repr=False)
class PollOption(Type):
    text: str
    voter_count: int
    text_entities: Optional[MessageEntity] = None
