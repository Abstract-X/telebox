from contextvars import ContextVar
from typing import TYPE_CHECKING

from telebox.typing import Event
if TYPE_CHECKING:
    from telebox.dispatcher.handlers.handlers.event import AbstractEventHandler
    from telebox.dispatcher.handlers.handlers.error import AbstractErrorHandler


event_context: ContextVar[Event] = ContextVar("event_context")
event_handler_context: ContextVar["AbstractEventHandler"] = ContextVar("event_handler_context")
error_handler_context: ContextVar["AbstractErrorHandler"] = ContextVar("error_handler_context")
