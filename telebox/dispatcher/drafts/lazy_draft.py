from typing import Optional
from threading import Lock

from telebox.dispatcher.drafts.storage import AbstractDraftStorage, Value


class LazyDraft:
    def __init__(
        self,
        storage: AbstractDraftStorage,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ):
        self._storage = storage
        self._chat_id = chat_id
        self._user_id = user_id
        self._draft: Optional[dict[str, Value]] = None
        self._draft_lock = Lock()
        self._is_changed = False

    def __getitem__(self, item: str) -> Value:
        self._lazy_load()

        return self._draft[item]

    def __setitem__(self, key: str, value: Value) -> None:
        self.set(field=key, value=value)

    def __delitem__(self, key: str) -> None:
        self.delete(field=key)

    def __iter__(self):
        self._lazy_load()

        return iter(self._draft)

    @property
    def is_changed(self) -> bool:
        with self._draft_lock:
            if self._draft is None:
                return False

            return self._is_changed

    def get(self, field: str, default: Value = None) -> Value:
        self._lazy_load()

        return self._draft.get(field, default)

    def set(self, field: str, value: Value) -> None:
        self._lazy_load()
        self._draft[field] = value
        self._is_changed = True

    def delete(self, field: str) -> None:
        self._lazy_load()
        del self._draft[field]
        self._is_changed = True

    def drop(self, field: str, default: Value = None) -> Value:
        self._lazy_load()

        if field in self._draft:
            value = self._draft.pop(field)
            self._is_changed = True

            return value

        return default

    def get_data(self) -> dict[str, Value]:
        self._lazy_load()

        return self._draft

    def _lazy_load(self) -> None:
        with self._draft_lock:
            if self._draft is None:
                self._draft = self._storage.load_draft(
                    chat_id=self._chat_id,
                    user_id=self._user_id
                )
