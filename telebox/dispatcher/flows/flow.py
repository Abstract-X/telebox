import copy

from telebox.dispatcher.flows.storage import Value


class Flow:
    def __init__(self, data: dict[str, Value]):
        self._data = data
        self._original_data = copy.deepcopy(data)

    def __getitem__(self, item: str) -> Value:
        return self._data[item]

    def __setitem__(self, key: str, value: Value) -> None:
        self.set(field=key, value=value)

    def __delitem__(self, key: str) -> None:
        self.delete(field=key)

    def __iter__(self):
        return iter(self._data)

    @property
    def is_changed(self) -> bool:
        return self._data != self._original_data

    def get(self, field: str, default: Value = None) -> Value:
        return self._data.get(field, default)

    def set(self, field: str, value: Value) -> None:
        self._data[field] = value

    def delete(self, field: str) -> None:
        del self._data[field]

    def pop(self, field: str, default: Value = None) -> Value:
        return self._data.pop(field, default)

    def clear(self) -> None:
        self._data.clear()

    def get_data(self) -> dict[str, Value]:
        return self._data
