from typing import Optional

from telebox.dispatcher.type_hints import Event, Handler, ErrorHandler
from telebox.dispatcher.enums.event_type import EventType
from telebox.utils.deps import Deps
from telebox.utils.data import Data


class Context:
    __slots__ = ("event", "event_type", "deps", "data", "chat_id", "user_id", "handler", "error", "error_handler")

    def __init__(
        self,
        event: Event,
        event_type: EventType,
        deps: Deps,
        chat_id: Optional[int] = None,
        user_id: Optional[int] = None
    ):
        self.event = event
        self.event_type = event_type
        self.deps = deps
        self.data = Data()
        self.chat_id = chat_id
        self.user_id = user_id
        self.handler: Optional[Handler] = None
        self.error: Optional[Exception] = None
        self.error_handler: Optional[ErrorHandler] = None
