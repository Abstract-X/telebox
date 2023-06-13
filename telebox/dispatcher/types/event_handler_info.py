from dataclasses import dataclass
from typing import Optional

from telebox.dispatcher.handlers.event import AbstractEventHandler
from telebox.dispatcher.filters.events.filter import AbstractEventBaseFilter
from telebox.dispatcher.utils.rate_limiter.rate_limiter import RateLimiter
from telebox.dispatcher.utils.rate_limiter.rate_limit import RateLimit


@dataclass
class EventHandlerInfo:
    handler: AbstractEventHandler
    filter: AbstractEventBaseFilter
    with_chat_waiting: bool
    rate_limiter: Optional[RateLimiter] = None

    @property
    def rate_limit(self) -> Optional[RateLimit]:
        return self.rate_limiter.limit if self.rate_limiter is not None else None
