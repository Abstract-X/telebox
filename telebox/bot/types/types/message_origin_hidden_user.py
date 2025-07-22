from datetime import datetime

from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class MessageOriginHiddenUser(Type):
    date: datetime
    sender_user_name: str
    type: str = "hidden_user"
