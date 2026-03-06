from typing import Any, Optional


class Data:
    def __init__(self, data: Optional[dict[str, Any]] = None):
        self._data = {} if data is None else data

    def __bool__(self):
        return bool(self._data)

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def __repr__(self):
        return f"{type(self).__name__}({self._data!r})"

    def set(self, field: str, value: Any) -> None:
        self._data[field] = value

    def get(self, field: str, default: Any = None) -> Any:
        return self._data.get(field, default)
