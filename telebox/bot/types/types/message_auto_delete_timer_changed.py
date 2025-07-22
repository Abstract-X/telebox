from attrs import define

from telebox.bot.types.type import Type


@define(repr=False)
class MessageAutoDeleteTimerChanged(Type):
    message_auto_delete_time: int
