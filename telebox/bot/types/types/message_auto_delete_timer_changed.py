from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(repr=False)
class MessageAutoDeleteTimerChanged(Type):
    message_auto_delete_time: int
