from typing import Union

from telebox.bot.types.types.background_fill_solid import BackgroundFillSolid
from telebox.bot.types.types.background_fill_gradient import BackgroundFillGradient
from telebox.bot.types.types.background_fill_freeform_gradient import BackgroundFillFreeformGradient


BackgroundFill = Union[BackgroundFillSolid,
                       BackgroundFillGradient,
                       BackgroundFillFreeformGradient]
