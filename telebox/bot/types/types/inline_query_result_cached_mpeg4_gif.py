from dataclasses import dataclass
from typing import Optional, Union

from telebox.bot.types.type import Type
from telebox.bot.consts import inline_query_result_types
from telebox.bot.types.types.message_entity import MessageEntity
from telebox.bot.types.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.bot.types.types.input_message_content import InputMessageContent
from telebox.utils.not_set import NotSet, NOT_SET


@dataclass(repr=False)
class InlineQueryResultCachedMpeg4Gif(Type):
    id: str
    mpeg4_file_id: str
    title: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Union[str, None, NotSet] = NOT_SET
    caption_entities: Optional[list[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
    type: str = inline_query_result_types.MPEG4_GIF
