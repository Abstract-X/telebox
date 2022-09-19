from typing import Union

from telebox.telegram_bot.types.types.input_media_photo import InputMediaPhoto
from telebox.telegram_bot.types.types.input_media_video import InputMediaVideo
from telebox.telegram_bot.types.types.input_media_animation import InputMediaAnimation
from telebox.telegram_bot.types.types.input_media_audio import InputMediaAudio
from telebox.telegram_bot.types.types.input_media_document import InputMediaDocument


InputMedia = Union[InputMediaPhoto,
                   InputMediaVideo,
                   InputMediaAnimation,
                   InputMediaAudio,
                   InputMediaDocument]
