from dataclasses import dataclass
from typing import Optional

from telebox.telegram.types.base import Type
from telebox.telegram.consts import inline_query_result_types
from telebox.telegram.types.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.telegram.types.types.input_message_content import InputMessageContent


@dataclass(unsafe_hash=True)
class InlineQueryResultCachedSticker(Type):
    id: str
    sticker_file_id: str
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
    type: str = inline_query_result_types.STICKER
