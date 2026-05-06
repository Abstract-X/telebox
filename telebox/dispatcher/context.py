from typing import Optional, TypeVar, Generic
from dataclasses import dataclass, field

from telebox.bot.bot import Bot
from telebox.ui.ui import UI
from telebox.dispatcher.state_machine import StateMachine
from telebox.dispatcher.drafts.lazy_draft import LazyDraft
from telebox.dispatcher.flows.manager import FlowManager
from telebox.dispatcher.type_hints import Event, Handler, ErrorHandler
from telebox.dispatcher.enums.event_type import EventType


ET = TypeVar("ET", bound=Event)


@dataclass
class EventContext(Generic[ET]):
    event: ET
    event_type: EventType
    chat_id: Optional[int] = None
    user_id: Optional[int] = None
    handler: Optional[Handler] = None
    error: Optional[Exception] = None
    error_handler: Optional[ErrorHandler] = None
    bot: Optional[Bot] = None
    ui: Optional[UI] = None
    state_machine: Optional[StateMachine] = None
    flow_manager: Optional[FlowManager] = None
    draft: Optional[LazyDraft] = None
    _flow_id: Optional[int] = field(default=None, init=False, repr=False)

    @property
    def flow_id(self) -> int:
        if self._flow_id is None:
            raise ValueError("flow_id is not set!")

        return self._flow_id

    @flow_id.setter
    def flow_id(self, value: int) -> None:
        self._flow_id = value
