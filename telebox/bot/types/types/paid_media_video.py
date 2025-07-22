from attrs import define

from telebox.bot.types.type import Type
from telebox.bot.consts import paid_media_types
from telebox.bot.types.types.video import Video


@define(repr=False)
class PaidMediaVideo(Type):
    video: Video
    type: str = paid_media_types.VIDEO
