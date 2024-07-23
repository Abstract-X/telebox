from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.consts import inline_query_result_types
from telebox.bot.types.types.message_entity import MessageEntity
from telebox.bot.types.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.bot.types.types.input_message_content import InputMessageContent


@dataclass(repr=False)
class InlineQueryResultMpeg4Gif(Type):
    id: str
    mpeg4_url: str
    thumbnail_url: str
    mpeg4_width: Optional[int] = None
    mpeg4_height: Optional[int] = None
    mpeg4_duration: Optional[int] = None
    thumbnail_mime_type: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[list[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
    type: str = inline_query_result_types.MPEG4_GIF
