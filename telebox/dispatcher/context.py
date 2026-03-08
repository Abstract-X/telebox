from typing import Optional, TypeVar, Generic

from telebox.dispatcher.drafts.lazy_draft import LazyDraft
from telebox.dispatcher.type_hints import Event, Handler, ErrorHandler
from telebox.dispatcher.enums.event_type import EventType
from telebox.bot.bot import Bot
from telebox.state_machine.machine import StateMachine
from telebox.deps import DepsBase


ET = TypeVar("ET", bound=Event)
DT = TypeVar("DT", bound=DepsBase)


class EventContext(Generic[ET, DT]):
    __slots__ = (
        "event",
        "event_type",
        "deps",
        "chat_id",
        "user_id",
        "bot",
        "state_machine",
        "draft",
        "data",
        "handler",
        "error",
        "error_handler"
    )

    def __init__(
        self,
        event: ET,
        event_type: EventType,
        deps: DT,
        *,
        chat_id: Optional[int] = None,
        user_id: Optional[int] = None,
        bot: Optional[Bot] = None,
        state_machine: Optional[StateMachine] = None,
        draft: Optional[LazyDraft] = None
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
        self.bot: Optional[Bot] = bot
        self.state_machine: Optional[StateMachine] = state_machine
        self.draft: Optional[LazyDraft] = draft
