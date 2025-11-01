from telebox.bot.utils.converter import converting_context
from telebox.utils.unset import UNSET


def default_factory():
    if converting_context.get():
        return None

    return UNSET
