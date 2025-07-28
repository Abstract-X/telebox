from typing import Optional

from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class KeyboardButtonPollType(Type):
    type: Optional[str] = None
