from abc import ABC, abstractmethod
from typing import Optional


class AbstractStateStorage(ABC):
    @abstractmethod
    def load_state_ids(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> Optional[list[int]]:
        pass

    @abstractmethod
    def load_flow_state_ids(
        self,
        *,
        flow_id: int
    ) -> Optional[list[int]]:
        pass

    @abstractmethod
    def save_state_transition(
        self,
        state_ids: list[int],
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        pass

    @abstractmethod
    def save_flow_state_transition(
        self,
        state_ids: list[int],
        *,
        flow_id: int,
        chat_id: int,
        user_id: Optional[int] = None,
        input_flow_id: Optional[int] = None
    ) -> None:
        pass

    @abstractmethod
    def load_current_state_ids(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> Optional[list[int]]:
        pass

    @abstractmethod
    def load_input_flow_id(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> Optional[int]:
        pass
