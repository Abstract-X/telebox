from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class WebAppInfo(Type):
    url: str
