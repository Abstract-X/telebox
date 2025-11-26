from dataclasses import dataclass

from telebox.dispatcher.middleware import Middleware
from telebox.dispatcher.type_hints import Handler


@dataclass
class MiddlewareInfo:
    middleware: Middleware
    handlers: list[Handler]
