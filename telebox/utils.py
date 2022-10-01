from dataclasses import dataclass
import dataclasses
from typing import Union, Iterable, Any


class NotSetValue:
    pass


@dataclass
class RequestTimeout:
    connect_secs: Union[float, int]
    read_secs: Union[float, int]


@dataclass
class Set:

    def __post_init__(self):
        fields = {i.name for i in dataclasses.fields(self)}
        self._items = {
            value
            for name, value in vars(self).items()
            if name in fields
        }

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __repr__(self):
        return f"{type(self).__name__}({self._items!r})"

    def __contains__(self, item):
        return item in self._items

    def get(self, *, exclude: Iterable[Any] = ()) -> set[Any]:
        return {i for i in self._items if i not in exclude}


NOT_SET_VALUE = NotSetValue()
