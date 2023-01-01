from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.inline_keyboard_button import InlineKeyboardButton


@dataclass(eq=False)
class InlineKeyboardMarkup(Type):
    inline_keyboard: list[list[InlineKeyboardButton]]
