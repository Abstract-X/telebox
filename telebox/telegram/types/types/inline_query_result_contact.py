from dataclasses import dataclass
from typing import Optional

from telebox.telegram.types.base import Type
from telebox.telegram.consts import inline_query_result_types
from telebox.telegram.types.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.telegram.types.types.input_message_content import InputMessageContent


@dataclass(unsafe_hash=True)
class InlineQueryResultContact(Type):
    id: str
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    vcard: Optional[str] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None
    input_message_content: Optional[InputMessageContent] = None
    thumb_url: Optional[str] = None
    thumb_width: Optional[int] = None
    thumb_height: Optional[int] = None
    type: str = inline_query_result_types.CONTACT
