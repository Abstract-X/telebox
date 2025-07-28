from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class WebAppData(Type):
    data: str
    button_text: str
