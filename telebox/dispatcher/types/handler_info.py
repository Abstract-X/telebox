from dataclasses import dataclass
from typing import Optional

from telebox.dispatcher.filters.filter import AbstractBaseFilter
from telebox.dispatcher.utils.rate_limiter.rate_limiter import RateLimiter
from telebox.dispatcher.utils.rate_limiter.rate_limit import RateLimit
from telebox.dispatcher.type_hints import Handler


@dataclass
class HandlerInfo:
    handler: Handler
    filter: AbstractBaseFilter
    with_chat_queue: bool
    rate_limiter: Optional[RateLimiter] = None

    @property
    def rate_limit(self) -> Optional[RateLimit]:
        return self.rate_limiter.limit if self.rate_limiter is not None else None
