from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class WebAppData(Type):
    data: str
    button_text: str
