from dataclasses import dataclass

from telebox.dispatcher.handlers.error import AbstractErrorHandler


@dataclass
class ErrorHandlerInfo:
    handler: AbstractErrorHandler
    error_type: type
