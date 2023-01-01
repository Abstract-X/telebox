from dataclasses import dataclass

from telebox.bot.types.type import Type
from telebox.bot.types.types.user import User


@dataclass(eq=False)
class VideoChatParticipantsInvited(Type):
    users: list[User]
