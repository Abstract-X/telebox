from typing import Optional
import copy

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
        self._data: Optional[dict[str, Value]] = None
        self._original_data: Optional[dict[str, Value]] = None

    def __getitem__(self, item: str) -> Value:
        self._lazy_load()

        return self._data[item]

    def __setitem__(self, key: str, value: Value) -> None:
        self.set(field=key, value=value)

    def __delitem__(self, key: str) -> None:
        self.delete(field=key)

    def __iter__(self):
        self._lazy_load()

        return iter(self._data)

    @property
    def is_loaded(self) -> bool:
        return self._data is not None

    @property
    def is_changed(self) -> bool:
        if not self.is_loaded:
            return False

        return self._data != self._original_data

    def get(self, field: str, default: Value = None) -> Value:
        self._lazy_load()

        return self._data.get(field, default)

    def set(self, field: str, value: Value) -> None:
        self._lazy_load()
        self._data[field] = value

    def delete(self, field: str) -> None:
        self._lazy_load()
        del self._data[field]

    def pop(self, field: str, default: Value = None) -> Value:
        self._lazy_load()

        return self._data.pop(field, default)

    def clear(self) -> None:
        self._lazy_load()
        self._data.clear()

    def get_data(self) -> dict[str, Value]:
        self._lazy_load()

        return self._data

    def _lazy_load(self) -> None:
        if not self.is_loaded:
            data = self._storage.load(chat_id=self._chat_id, user_id=self._user_id)
            self._data = copy.deepcopy(data)
            self._original_data = data
