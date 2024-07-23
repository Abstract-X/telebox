from typing import Union

from telebox.bot.types.types.input_paid_media_photo import InputPaidMediaPhoto
from telebox.bot.types.types.input_paid_media_video import InputPaidMediaVideo


InputPaidMedia = Union[InputPaidMediaPhoto,
                       InputPaidMediaVideo]
