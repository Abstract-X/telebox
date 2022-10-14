from contextvars import ContextVar

from telebox.typing import Event
from telebox.dispatcher.handlers.handlers.event import AbstractEventHandler
from telebox.dispatcher.handlers.handlers.error import AbstractErrorHandler


event_context: ContextVar[Event] = ContextVar("event_context")
event_handler_context: ContextVar[AbstractEventHandler] = ContextVar("event_handler_context")
error_handler_context: ContextVar[AbstractErrorHandler] = ContextVar("error_handler_context")
