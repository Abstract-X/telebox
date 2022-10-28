from typing import Union, Optional
from dataclasses import dataclass


@dataclass
class Limit:
    calls: int
    secs: Union[int, float]

    def __post_init__(self):
        if self.calls <= 0:
            raise ValueError(f"Calls must be greater than zero!")

        if self.secs <= 0:
            raise ValueError(f"Seconds must be greater than zero!")


class RateLimit:

    def __init__(
        self,
        *,
        chat_limit: Optional[Limit] = None,
        user_limit: Optional[Limit] = None,
        chat_user_limit: Optional[Limit] = None
    ):
        if all(i is None for i in (chat_limit, user_limit, chat_user_limit)):
            raise ValueError("No limits!")

        self._chat_limit = chat_limit
        self._user_limit = user_limit
        self._chat_user_limit = chat_user_limit

    @property
    def chat_limit_secs(self) -> Optional[int]:
        return self._chat_limit.secs if self.check_chat_limit() else None

    @property
    def user_limit_secs(self) -> Optional[int]:
        return self._user_limit.secs if self.check_user_limit() else None

    @property
    def chat_user_limit_secs(self) -> Optional[int]:
        return self._chat_user_limit.secs if self.check_chat_user_limit() else None

    @property
    def chat_limit_calls(self) -> Optional[int]:
        return self._chat_limit.calls if self.check_chat_limit() else None

    @property
    def user_limit_calls(self) -> Optional[int]:
        return self._user_limit.calls if self.check_user_limit() else None

    @property
    def chat_user_limit_calls(self) -> Optional[int]:
        return self._chat_user_limit.calls if self.check_chat_user_limit() else None

    def check_chat_limit(self) -> bool:
        return self._chat_limit is not None

    def check_user_limit(self) -> bool:
        return self._user_limit is not None

    def check_chat_user_limit(self) -> bool:
        return self._chat_user_limit is not None

    def process_chat_over_limit(self, chat_id: int) -> None:
        pass

    def process_user_over_limit(self, user_id: int) -> None:
        pass

    def process_chat_user_over_limit(self, chat_id: int, user_id: int) -> None:
        pass
