from typing import Union

from telebox.utils.callback_data_builders.builder import AbstractCallbackDataBuilder
from telebox.utils.serialization import get_serialized_data, get_deserialized_data


Key = Union[str, int]
Value = Union[str, int, float, bool, list, None]


class JSONCallbackDataBuilder(AbstractCallbackDataBuilder):

    def get_string(self, key: Key, value: Value = None) -> str:
        return get_serialized_data([key, value])

    def get_data(self, string: str) -> tuple[Key, Value]:
        return tuple(
            get_deserialized_data(string)
        )
