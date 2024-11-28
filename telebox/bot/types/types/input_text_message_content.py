from dataclasses import dataclass
from typing import Optional, Union

from telebox.bot.types.type import Type
from telebox.bot.types.types.message_entity import MessageEntity
from telebox.bot.types.types.link_preview_options import LinkPreviewOptions
from telebox.utils.not_set import NotSet, NOT_SET


@dataclass(repr=False)
class InputTextMessageContent(Type):
    message_text: str
    parse_mode: Union[str, None, NotSet] = NOT_SET
    entities: Optional[list[MessageEntity]] = None
    link_preview_options: Optional[LinkPreviewOptions] = None
