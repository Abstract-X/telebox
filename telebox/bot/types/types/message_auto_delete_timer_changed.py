from dataclasses import dataclass

from telebox.bot.types.type import Type


@dataclass(unsafe_hash=True)
class MessageAutoDeleteTimerChanged(Type):
    message_auto_delete_time: int
