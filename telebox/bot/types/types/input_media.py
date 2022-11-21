from typing import Union

from telebox.bot.types.types.input_media_photo import InputMediaPhoto
from telebox.bot.types.types.input_media_video import InputMediaVideo
from telebox.bot.types.types.input_media_animation import InputMediaAnimation
from telebox.bot.types.types.input_media_audio import InputMediaAudio
from telebox.bot.types.types.input_media_document import InputMediaDocument


InputMedia = Union[InputMediaPhoto,
                   InputMediaVideo,
                   InputMediaAnimation,
                   InputMediaAudio,
                   InputMediaDocument]
