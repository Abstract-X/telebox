from typing import Any, Union, Optional


Value = Union[str, int, float, bool, None]


class Draft:
    def __init__(self, data: Optional[dict[str, Value]] = None):
        self._data = data if data is not None else {}
        self._is_changed = False

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
        return self._is_changed

    def get(self, field: str, default: Value = None) -> Any:
        return self._data.get(field, default)

    def set(self, field: str, value: Value) -> None:
        self._data[field] = value
        self._is_changed = True

    def delete(self, field: str) -> None:
        del self._data[field]
        self._is_changed = True

    def drop(self, field: str, default: Value = None) -> Value:
        if field in self._data:
            value = self._data.pop(field)
            self._is_changed = True

            return value

        return default

    def get_data(self) -> dict[str, Value]:
        return self._data
