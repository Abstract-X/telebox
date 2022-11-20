from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.inline_keyboard_button import InlineKeyboardButton


@dataclass(unsafe_hash=True)
class InlineKeyboardMarkup(Type):
    inline_keyboard: list[list[InlineKeyboardButton]]
