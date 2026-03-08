from typing import Optional
from threading import Lock

from telebox.dispatcher.drafts.storage import AbstractDraftStorage, Value


class MemoryDraftStorage(AbstractDraftStorage):
    def __init__(self):
        self._drafts: dict[tuple[int, Optional[int]], dict[str, Value]] = {}
        self._lock = Lock()

    def save_draft(
        self,
        draft: dict[str, Value],
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        with self._lock:
            self._drafts[(chat_id, user_id)] = draft.copy()

    def load_draft(
        self,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> dict[str, Value]:
        with self._lock:
            draft = self._drafts.get((chat_id, user_id))

            if draft is not None:
                return draft.copy()

        return {}

    def clear_draft(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        with self._lock:
            self._drafts.pop((chat_id, user_id), None)
