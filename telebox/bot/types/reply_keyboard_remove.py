from typing import Literal, Optional

from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class ReplyKeyboardRemove(Type):
    remove_keyboard: Literal[True] = True
    selective: Optional[bool] = None
