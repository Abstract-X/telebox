from typing import Optional, Union

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.message_entity import MessageEntity


@define(repr=False)
class ReplyParameters(Type):
    message_id: int
    chat_id: Union[int, str, None] = None
    allow_sending_without_reply: Optional[bool] = None
    quote: Optional[str] = None
    quote_parse_mode: Optional[str] = None
    quote_entities: Optional[list[MessageEntity]] = None
    quote_position: Optional[int] = None
