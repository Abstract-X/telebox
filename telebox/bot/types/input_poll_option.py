from typing import Optional, Union

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.message_entity import MessageEntity
from telebox.utils.not_set import NotSet, NOT_SET


@define(repr=False)
class InputPollOption(Type):
    text: str
    text_parse_mode: Union[str, None, NotSet] = NOT_SET
    text_entities: Optional[list[MessageEntity]] = None
