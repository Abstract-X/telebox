from dataclasses import dataclass
from typing import Optional

from telebox.telegram_bot.types.type import Type


@dataclass(unsafe_hash=True)
class WebhookInfo(Type):
    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: Optional[str] = None
    last_error_date: Optional[int] = None
    last_error_message: Optional[str] = None
    last_synchronization_error_date: Optional[int] = None
    max_connections: Optional[int] = None
    allowed_updates: Optional[list[str]] = None
