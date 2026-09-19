from abc import ABC, abstractmethod
from typing import Union, Optional, Any


Value = Union[str, int, float, bool, list["Value"], dict[str, "Value"], None]


class AbstractFlowStorage(ABC):
    @abstractmethod
    def create(self, *, chat_id: int, user_id: Optional[int] = None, parent_flow_id: Optional[int] = None) -> int:
        pass

    @abstractmethod
    def finish(self, flow_id: int) -> None:
        pass

    @abstractmethod
    def save(self, flow_id: int, data: Optional[dict[str, Any]] = None) -> None:
        pass

    @abstractmethod
    def load(self, flow_id: int) -> tuple[Optional[dict[str, Any]], Optional[int]]:
        pass
