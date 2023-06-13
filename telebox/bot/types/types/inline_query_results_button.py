from dataclasses import dataclass
from typing import Optional

from telebox.bot.types.type import Type
from telebox.bot.types.types.web_app_info import WebAppInfo


@dataclass
class InlineQueryResultsButton(Type):
    text: str
    web_app: Optional[WebAppInfo] = None
    start_parameter: Optional[str] = None
