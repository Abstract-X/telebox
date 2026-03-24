from typing import Optional
from threading import Lock

from telebox.dispatcher.drafts.storage import AbstractDraftStorage


class MemoryDraftStorage(AbstractDraftStorage):
    def __init__(self):
        self._drafts: dict[tuple[int, Optional[int]], bytes] = {}
        self._lock = Lock()

    def _save(
        self,
        data: bytes,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        with self._lock:
            self._drafts[(chat_id, user_id)] = data

    def _load(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> Optional[bytes]:
        with self._lock:
            return self._drafts.get((chat_id, user_id))

    def delete(self, *, chat_id: int, user_id: Optional[int] = None) -> None:
        self._drafts.pop((chat_id, user_id), None)
