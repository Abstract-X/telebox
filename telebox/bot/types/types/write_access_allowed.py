from typing import Optional

from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class WriteAccessAllowed(Type):
    from_request: Optional[bool] = None
    web_app_name: Optional[str] = None
    from_attachment_menu: Optional[bool] = None
