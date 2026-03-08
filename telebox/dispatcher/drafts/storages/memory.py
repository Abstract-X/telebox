from typing import Any, Optional
from threading import Lock

from telebox.dispatcher.drafts.storage import AbstractDraftStorage


class MemoryDraftStorage(AbstractDraftStorage):
    def __init__(self):
        self._drafts = {}
        self._lock = Lock()

    def _save_draft(
        self,
        draft: dict[str, Any],
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        with self._lock:
            try:
                self._drafts[chat_id][user_id] = draft.copy()
            except KeyError:
                self._drafts[chat_id] = {
                    user_id: draft.copy()
                }

    def _load_draft(
        self,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> Optional[dict[str, Any]]:
        with self._lock:
            try:
                return self._drafts[chat_id][user_id].copy()
            except KeyError:
                return None
