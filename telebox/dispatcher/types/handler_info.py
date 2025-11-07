from dataclasses import dataclass

from telebox.dispatcher.filters.filter import AbstractBaseFilter
from telebox.dispatcher.type_hints import Handler


@dataclass
class HandlerInfo:
    handler: Handler
    filter: AbstractBaseFilter
    with_chat_queue: bool
