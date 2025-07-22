from typing import Optional

from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class LoginUrl(Type):
    url: str
    forward_text: Optional[str] = None
    bot_username: Optional[str] = None
    request_write_access: Optional[bool] = None
