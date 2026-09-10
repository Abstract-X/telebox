from abc import ABC, abstractmethod
from typing import Optional


class AbstractStateBundleStorage(ABC):
    @abstractmethod
    def save(
        self,
        magazine: list[int],
        *,
        chat_id: int,
        user_id: Optional[int] = None,
        flow_id: Optional[int] = None
    ) -> None:
        pass

    @abstractmethod
    def load(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> tuple[Optional[list[int]], Optional[int]]:
        pass
