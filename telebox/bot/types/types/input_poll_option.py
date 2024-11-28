from dataclasses import dataclass
from typing import Optional, Union

from telebox.bot.types.type import Type
from telebox.bot.types.types.message_entity import MessageEntity
from telebox.utils.not_set import NotSet, NOT_SET


@dataclass(repr=False)
class InputPollOption(Type):
    text: str
    text_parse_mode: Union[str, None, NotSet] = NOT_SET
    text_entities: Optional[list[MessageEntity]] = None
