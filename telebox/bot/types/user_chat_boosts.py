from attrs import define

from telebox.bot.type import Type
from telebox.bot.types.chat_boost import ChatBoost


@define(repr=False)
class UserChatBoosts(Type):
    boosts: list[ChatBoost]
