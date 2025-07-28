from datetime import datetime

from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class VideoChatScheduled(Type):
    start_date: datetime
