from dataclasses import dataclass

from telebox.dispatcher.filter import AbstractBaseFilter
from telebox.dispatcher.type_hints import Handler


@dataclass
class HandlerInfo:
    handler: Handler
    filter: AbstractBaseFilter
    use_chat_queue: bool
