from dataclasses import dataclass

from telebox.telegram_bot.types.base import Type


@dataclass(unsafe_hash=True)
class MessageAutoDeleteTimerChanged(Type):
    message_auto_delete_time: int