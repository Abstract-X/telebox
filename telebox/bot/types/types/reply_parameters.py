from dataclasses import dataclass
from typing import Optional, Union

from telebox.bot.types.type import Type
from telebox.bot.types.types.message_entity import MessageEntity


@dataclass
class ReplyParameters(Type):
    message_id: int
    chat_id: Union[int, str, None] = None
    allow_sending_without_reply: Optional[bool] = None
    quote: Optional[str] = None
    quote_parse_mode: Optional[str] = None
    quote_entities: Optional[list[MessageEntity]] = None
    quote_position: Optional[int] = None
