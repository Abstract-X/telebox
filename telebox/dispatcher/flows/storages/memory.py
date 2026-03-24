from typing import Optional
from threading import Lock

from telebox.dispatcher.flows.storage import AbstractFlowStorage


class MemoryFlowStorage(AbstractFlowStorage):
    def __init__(self):
        self._flows: dict[int, tuple[int, Optional[int], Optional[bytes]]] = {}
        self._lock = Lock()
        self._next_id = 1

    def create(self, *, chat_id: int, user_id: Optional[int] = None) -> int:
        with self._lock:
            flow_id = self._next_id
            self._next_id += 1
            self._flows[flow_id] = (chat_id, user_id, None)

            return flow_id

    def finish(self, flow_id: int) -> None:
        with self._lock:
            self._flows.pop(flow_id, None)

    def check(self, flow_id: int) -> bool:
        with self._lock:
            return flow_id in self._flows

    def _save(self, flow_id: int, data: Optional[bytes] = None) -> None:
        with self._lock:
            stored_flow = self._flows.get(flow_id)

            if stored_flow is None:
                return

            self._flows[flow_id] = (stored_flow[0], stored_flow[1], data)

    def _load(self, flow_id: int) -> Optional[bytes]:
        with self._lock:
            flow = self._flows.get(flow_id)

            if flow:
                return flow[2]
