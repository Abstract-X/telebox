from typing import Optional, TypeVar, Generic

from telebox.dispatcher.type_hints import Event, Handler, ErrorHandler
from telebox.dispatcher.enums.event_type import EventType
from telebox.deps import DepsBase


ET = TypeVar("ET", bound=Event)
DT = TypeVar("DT", bound=DepsBase)


class EventContext(Generic[ET, DT]):
    __slots__ = ("event", "event_type", "deps", "data", "chat_id", "user_id", "handler", "error", "error_handler")

    def __init__(
        self,
        event: ET,
        event_type: EventType,
        deps: DT,
        chat_id: Optional[int] = None,
        user_id: Optional[int] = None
    ):
        self.event: ET = event
        self.event_type: EventType = event_type
        self.deps: DT = deps
        self.data: dict = {}
        self.chat_id: Optional[int] = chat_id
        self.user_id: Optional[int] = user_id
        self.handler: Optional[Handler] = None
        self.error: Optional[Exception] = None
        self.error_handler: Optional[ErrorHandler] = None


class StateContext(Generic[DT]):
    __slots__ = ("deps", "chat_id", "user_id", "data")

    def __init__(
        self,
        deps: DT,
        chat_id: int,
        user_id: Optional[int] = None,
        data: Optional[dict] = None
    ):
        self.deps: DT = deps
        self.chat_id: int = chat_id
        self.user_id: Optional[int] = user_id
        self.data: dict = data if data is not None else {}
