from datetime import datetime

from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class VideoChatScheduled(Type):
    start_date: datetime
