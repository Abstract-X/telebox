from datetime import datetime
from typing import Optional

from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.web_app_user import WebAppUser
from telebox.bot.types.web_app_chat import WebAppChat


@define(repr=False)
class WebAppInitData(Type):
    auth_date: datetime
    hash: str
    query_id: Optional[str] = None
    user: Optional[WebAppUser] = None
    receiver: Optional[WebAppUser] = None
    chat: Optional[WebAppChat] = None
    chat_type: Optional[str] = None
    chat_instance: Optional[str] = None
    start_param: Optional[str] = None
    can_send_after: Optional[int] = None
