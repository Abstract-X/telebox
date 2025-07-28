from datetime import datetime

from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class PassportFile(Type):
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: datetime
