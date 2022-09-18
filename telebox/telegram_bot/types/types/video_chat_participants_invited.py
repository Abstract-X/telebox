from dataclasses import dataclass

from telebox.telegram_bot.types.base import Type
from telebox.telegram_bot.types.types.user import User


@dataclass(unsafe_hash=True)
class VideoChatParticipantsInvited(Type):
    users: list[User]