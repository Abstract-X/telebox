import copy
from typing import Optional

from telebox.dispatcher.flows.storage import Value


class Flow:
    def __init__(self, id_: int, data: Optional[dict[str, Value]] = None):
        self.id = id_
        self.data = data or {}
        self._original_data = copy.deepcopy(data)

    def __getitem__(self, item: str) -> Value:
        return self.data[item]

    def __setitem__(self, key: str, value: Value) -> None:
        self.set(field=key, value=value)

    def __delitem__(self, key: str) -> None:
        self.delete(field=key)

    def __iter__(self):
        return iter(self.data)

    @property
    def is_changed(self) -> bool:
        return self.data != self._original_data

    def get(self, field: str, default: Value = None) -> Value:
        return self.data.get(field, default)

    def set(self, field: str, value: Value) -> None:
        self.data[field] = value

    def delete(self, field: str) -> None:
        del self.data[field]

    def pop(self, field: str, default: Value = None) -> Value:
        return self.data.pop(field, default)

    def clear(self) -> None:
        self.data.clear()
