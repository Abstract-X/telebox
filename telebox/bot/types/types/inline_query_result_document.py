from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.consts import inline_query_result_types
from telebox.bot.types.types.message_entity import MessageEntity
from telebox.bot.types.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.bot.types.types.input_message_content import InputMessageContent


@dataclass
class InlineQueryResultDocument(Type):
    id: str
    title: str
    document_url: str
    mime_type: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[list[MessageEntity]] = None
    description: Optional[str] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
    thumbnail_url: Optional[str] = None
    thumbnail_width: Optional[int] = None
    thumbnail_height: Optional[int] = None
    type: str = inline_query_result_types.DOCUMENT
