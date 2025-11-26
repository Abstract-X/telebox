from dataclasses import dataclass

from telebox.dispatcher.type_hints import ErrorHandler


@dataclass
class ErrorHandlerInfo:
    handler: ErrorHandler
    error_type: type[Exception]
