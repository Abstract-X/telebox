from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.user import User


@define(repr=False)
class VideoChatParticipantsInvited(Type):
    users: list[User]
