from typing import Iterable, Union

from telebox.utils.callback_data_builders.builder import AbstractCallbackDataBuilder


Key = str
Value = Union[str, Iterable[str], None]


class SeparatoryCallbackDataBuilder(AbstractCallbackDataBuilder):

    def __init__(self, separator: str):
        if not separator:
            raise ValueError(f"Invalid separator {separator!r}!")

        self._separator = separator

    def get_builded_data(self, key: Key, value: Value = None) -> str:
        if self._separator in key:
            raise ValueError(f"Key {key!r} contains separator {self._separator!r}!")

        data = key

        if value is not None:
            if isinstance(value, str):
                value = [value]

            for i in value:
                if self._separator in i:
                    raise ValueError(f"Value {i!r} contains separator {self._separator!r}!")

                data += f"{self._separator}{i}"

        return data

    def get_parsed_data(self, data: str) -> tuple[Key, Value]:
        key, *value = data.split(self._separator)

        if not value:
            value = None
        elif len(value) == 1:
            value = value[0]

        return key, value
