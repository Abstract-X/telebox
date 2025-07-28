from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class VideoChatStarted(Type):
    pass
