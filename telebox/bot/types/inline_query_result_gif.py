from typing import Optional, Union

from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import inline_query_result_types
from telebox.bot.types.message_entity import MessageEntity
from telebox.bot.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.bot.types.input_message_content import InputMessageContent
from telebox.utils.not_set import NotSet, NOT_SET


@define(repr=False)
class InlineQueryResultGif(Type):
    id: str
    gif_url: str
    thumbnail_url: str
    gif_width: Optional[int] = None
    gif_height: Optional[int] = None
    gif_duration: Optional[int] = None
    thumbnail_mime_type: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Union[str, None, NotSet] = NOT_SET
    caption_entities: Optional[list[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
    type: str = inline_query_result_types.GIF
