from typing import Optional
from threading import Lock

from telebox.dispatcher.state_machine.storage import AbstractStateBundleStorage


class MemoryStateBundleStorage(AbstractStateBundleStorage):
    def __init__(self):
        self._bundles: dict[tuple[int, Optional[int]], tuple[list[str], Optional[int]]] = {}
        self._lock = Lock()

    def save(
        self,
        magazine: list[str],
        *,
        chat_id: int,
        user_id: Optional[int] = None,
        flow_id: Optional[int] = None
    ) -> None:
        with self._lock:
            self._bundles[(chat_id, user_id)] = (magazine[:], flow_id)

    def load(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> tuple[Optional[list[str]], Optional[int]]:
        with self._lock:
            magazine, flow_id = self._bundles.get((chat_id, user_id))

            return magazine[:], flow_id
