from typing import Optional

from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.types.types.web_app_info import WebAppInfo


@define(repr=False)
class InlineQueryResultsButton(Type):
    text: str
    web_app: Optional[WebAppInfo] = None
    start_parameter: Optional[str] = None
