from abc import ABC, abstractmethod
from typing import Optional, Union


Value = Union[str, int, float, bool, None]


class AbstractDraftStorage(ABC):
    @abstractmethod
    def save_draft(
        self,
        draft: dict[str, Value],
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        pass

    @abstractmethod
    def load_draft(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> dict[str, Value]:
        pass

    @abstractmethod
    def clear_draft(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        pass
