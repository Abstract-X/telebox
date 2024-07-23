from typing import Union

from telebox.bot.types.types.paid_media_preview import PaidMediaPreview
from telebox.bot.types.types.paid_media_photo import PaidMediaPhoto
from telebox.bot.types.types.paid_media_video import PaidMediaVideo


PaidMedia = Union[PaidMediaPreview,
                  PaidMediaPhoto,
                  PaidMediaVideo]
