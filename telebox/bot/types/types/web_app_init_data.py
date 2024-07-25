from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.web_app_user import WebAppUser
from telebox.bot.types.types.web_app_chat import WebAppChat


@dataclass(repr=False)
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
