from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.consts import inline_query_result_types
from telebox.bot.types.types.inline_keyboard_markup import InlineKeyboardMarkup


@dataclass(eq=False)
class InlineQueryResultGame(Type):
    id: str
    game_short_name: str
    reply_markup: Optional[InlineKeyboardMarkup] = None
    type: str = inline_query_result_types.GAME
