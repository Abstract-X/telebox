from dataclasses import dataclass
from typing import Literal, Optional

from telebox.telegram_bot.types.base import Type


@dataclass(unsafe_hash=True)
class ReplyKeyboardRemove(Type):
    remove_keyboard: Literal[True] = True
    selective: Optional[bool] = None
