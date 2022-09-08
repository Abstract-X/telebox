from dataclasses import dataclass
from typing import Optional

from telebox.telegram.types.base import Type
from telebox.telegram.consts import inline_query_result_types
from telebox.telegram.types.types.inline_keyboard_markup import InlineKeyboardMarkup


@dataclass(unsafe_hash=True)
class InlineQueryResultGame(Type):
    id: str
    game_short_name: str
    reply_markup: Optional[InlineKeyboardMarkup] = None
    type: str = inline_query_result_types.GAME
