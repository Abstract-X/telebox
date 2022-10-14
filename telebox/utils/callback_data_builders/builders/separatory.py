from typing import Iterable, Union

from telebox.utils.callback_data_builders.base import AbstractCallbackDataBuilder


FilterKey = str
Value = Union[str, Iterable[str], None]


class SeparatoryCallbackDataBuilder(AbstractCallbackDataBuilder):

    def __init__(self, separator: str):
        if not separator:
            raise ValueError(f"Invalid separator {separator!r}!")

        self._separator = separator

    def build(self, filter_key: FilterKey, value: Value = None) -> str:
        if self._separator in filter_key:
            raise ValueError(f"Filter key {filter_key!r} contains separator {self._separator!r}!")

        data = filter_key

        if value is not None:
            if isinstance(value, str):
                value = [value]

            for i in value:
                if self._separator in i:
                    raise ValueError(f"Value {i!r} contains separator {self._separator!r}!")

                data += f"{self._separator}{i}"

        return data

    def parse(self, data: str) -> tuple[FilterKey, Value]:
        filter_key, *value = data.split(self._separator)

        if not value:
            value = None
        elif len(value) == 1:
            value = value[0]

        return filter_key, value
