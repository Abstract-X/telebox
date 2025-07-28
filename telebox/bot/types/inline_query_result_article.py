from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.consts import inline_query_result_types
from telebox.bot.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.bot.types.input_message_content import InputMessageContent


@define(repr=False)
class InlineQueryResultArticle(Type):
    id: str
    title: str
    input_message_content: InputMessageContent
    reply_markup: Optional[InlineKeyboardMarkup] = None
    url: Optional[str] = None
    hide_url: Optional[bool] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    thumbnail_width: Optional[int] = None
    thumbnail_height: Optional[int] = None
    type: str = inline_query_result_types.ARTICLE
