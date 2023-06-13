from dataclasses import dataclass

from telebox.dispatcher.handlers.error import AbstractErrorHandler
from telebox.dispatcher.filters.errors.filter import AbstractErrorBaseFilter


@dataclass
class ErrorHandlerInfo:
    handler: AbstractErrorHandler
    filter: AbstractErrorBaseFilter
