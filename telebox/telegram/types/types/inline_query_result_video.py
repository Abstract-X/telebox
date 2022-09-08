from dataclasses import dataclass
from typing import Optional

from telebox.telegram.types.base import Type
from telebox.telegram.consts import inline_query_result_types
from telebox.telegram.types.types.message_entity import MessageEntity
from telebox.telegram.types.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.telegram.types.types.input_message_content import InputMessageContent


@dataclass(unsafe_hash=True)
class InlineQueryResultVideo(Type):
    id: str
    video_url: str
    mime_type: str
    thumb_url: str
    title: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[list[MessageEntity]] = None
    video_width: Optional[int] = None
    video_height: Optional[int] = None
    video_duration: Optional[int] = None
    description: Optional[str] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
    type: str = inline_query_result_types.VIDEO
