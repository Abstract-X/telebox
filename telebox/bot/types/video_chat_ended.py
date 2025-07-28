from attrs import define

from telebox.bot.type import Type


@define(repr=False)
class VideoChatEnded(Type):
    duration: int
