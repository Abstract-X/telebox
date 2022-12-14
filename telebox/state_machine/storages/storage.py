from abc import ABC, abstractmethod
from typing import Optional


class AbstractStateStorage(ABC):

    @abstractmethod
    def save_states(
        self,
        states: list[str],
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        pass

    @abstractmethod
    def load_states(self, *, chat_id: int, user_id: Optional[int] = None) -> list[str]:
        pass
