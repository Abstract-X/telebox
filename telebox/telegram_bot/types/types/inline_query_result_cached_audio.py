from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.consts import inline_query_result_types
from telebox.telegram_bot.types.types.message_entity import MessageEntity
from telebox.telegram_bot.types.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.telegram_bot.types.types.input_message_content import InputMessageContent


@dataclass(unsafe_hash=True)
class InlineQueryResultCachedAudio(Type):
    id: str
    audio_file_id: str
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[list[MessageEntity]] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
    type: str = inline_query_result_types.AUDIO
