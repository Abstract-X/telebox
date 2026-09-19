import copy
from dataclasses import dataclass
from typing import Optional, Any
from threading import Lock

from telebox.dispatcher.flows.storage import AbstractFlowStorage


@dataclass
class Record:
    chat_id: int
    user_id: Optional[int] = None
    data: Optional[dict[str, Any]] = None
    parent_id: Optional[int] = None


class MemoryFlowStorage(AbstractFlowStorage):
    def __init__(self):
        self._records: dict[int, Record] = {}
        self._lock = Lock()
        self._next_id = 1

    def create(self, *, chat_id: int, user_id: Optional[int] = None, parent_flow_id: Optional[int] = None) -> int:
        with self._lock:
            flow_id = self._next_id
            self._next_id += 1
            self._records[flow_id] = Record(chat_id=chat_id, user_id=user_id, parent_id=parent_flow_id)

            return flow_id

    def finish(self, flow_id: int) -> None:
        with self._lock:
            self._records.pop(flow_id, None)

    def save(self, flow_id: int, data: Optional[dict[str, Any]] = None) -> None:
        with self._lock:
            record = self._records.get(flow_id)

            if record is not None:
                record.data = copy.deepcopy(data)

    def load(self, flow_id: int) -> tuple[Optional[dict[str, Any]], Optional[int]]:
        with self._lock:
            record = self._records.get(flow_id)

            if record is not None:
                return record.data, record.parent_id

            return None, None
