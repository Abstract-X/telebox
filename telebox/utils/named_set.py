from dataclasses import dataclass
import dataclasses
from typing import Any


@dataclass
class NamedSet:

    def __post_init__(self):
        self._items = _get_items(self)

    def __len__(self):
        return len(self._items)

    def __bool__(self):
        return bool(self._items)

    def __iter__(self):
        return iter(self._items)

    def __repr__(self):
        return f"{type(self).__name__}({self._items!r})"

    def __contains__(self, item):
        return item in self._items

    def get(self, *excluded: Any) -> set[Any]:
        return {i for i in self._items if i not in excluded}


def _get_items(set_: NamedSet) -> set[Any]:
    items = set()
    fields = {i.name for i in dataclasses.fields(set_)}

    for name, value in vars(set_).items():
        if name in fields:
            if isinstance(value, NamedSet):
                items.update(
                    _get_items(value)
                )
            else:
                items.add(value)

    return items
