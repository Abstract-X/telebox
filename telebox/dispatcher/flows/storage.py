from abc import ABC, abstractmethod
from typing import Union, Optional

from telebox.dispatcher.flows.errors import FlowNotFoundError
from telebox.utils import get_serialized_data, get_deserialized_data


Value = Union[str, int, float, bool, list["Value"], dict[str, "Value"], None]


class AbstractFlowStorage(ABC):
    @abstractmethod
    def create(self, *, chat_id: int, user_id: Optional[int] = None) -> int:
        pass

    @abstractmethod
    def finish(self, flow_id: int) -> None:
        pass

    @abstractmethod
    def check(self, flow_id: int) -> bool:
        pass

    @abstractmethod
    def _save(self, flow_id: int, data: Optional[bytes] = None) -> None:
        pass

    @abstractmethod
    def _load(self, flow_id: int) -> Optional[bytes]:
        pass

    def save(
        self,
        flow_id: int,
        data: dict[str, Value]
    ) -> None:
        self._save(
            flow_id=flow_id,
            data=get_serialized_data(data) if data else None
        )

    def load(self, flow_id: int) -> dict[str, Value]:
        if not self.check(flow_id):
            raise FlowNotFoundError(f"Flow with ID {flow_id} not found!")

        data = self._load(flow_id=flow_id)

        return get_deserialized_data(data) if data else {}
